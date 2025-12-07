#!/usr/bin/env python3
"""
Tool Generator

Takes a capability gap and generates a tool to address it.
This is the key to exponential improvement:
- Gap detector finds what's missing
- Tool generator creates what's needed
- Each generated tool makes future tool generation easier

Uses Claude API to generate tools, then validates them.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple
from datetime import datetime

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

TOOLS_DIR = Path(__file__).parent
GENERATED_LOG = TOOLS_DIR / "generated_tools.json"

# Templates for different tool types
TOOL_TEMPLATES = {
    "verification": '''
def verify_{name}(input_data, constraints):
    """Verify {description}"""
    results = []
    for constraint in constraints:
        # Check each constraint computationally
        passed = check_constraint(input_data, constraint)
        results.append({{"constraint": constraint, "passed": passed}})
    return results
''',
    "computation": '''
def compute_{name}(inputs):
    """Compute {description}"""
    # Show all work
    steps = []
    result = inputs
    # Computation here
    return {{"result": result, "steps": steps}}
''',
    "reasoning": '''
def reason_{name}(problem):
    """Structured reasoning for {description}"""
    # Externalize all steps
    premises = extract_premises(problem)
    inferences = []
    for premise in premises:
        inference = derive_from(premise)
        inferences.append(inference)
    conclusion = synthesize(inferences)
    return {{"premises": premises, "inferences": inferences, "conclusion": conclusion}}
'''
}


@dataclass
class GeneratedTool:
    name: str
    purpose: str
    code: str
    file_path: str
    generated_at: str
    from_gap: Optional[str]
    validated: bool
    validation_result: Optional[str]


class ToolGenerator:
    """Generates tools from capability gap descriptions."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.generated: list = []
        self._load_history()

    def _load_history(self):
        """Load history of generated tools."""
        if GENERATED_LOG.exists():
            try:
                data = json.loads(GENERATED_LOG.read_text())
                self.generated = data
            except:
                self.generated = []

    def _save_history(self):
        """Save generation history."""
        GENERATED_LOG.write_text(json.dumps(self.generated, indent=2))

    def generate_from_gap(
        self,
        gap_type: str,
        description: str,
        evidence: str,
        suggested_name: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Generate a tool to address a capability gap.

        Returns: (tool_code, file_path)
        """
        if not HAS_ANTHROPIC or not self.api_key:
            # Fallback to template-based generation
            return self._generate_from_template(gap_type, description, suggested_name)

        # Use Claude to generate a sophisticated tool
        client = anthropic.Anthropic(api_key=self.api_key)

        prompt = f"""Generate a COMPLETE, WORKING Python tool to address this capability gap:

GAP TYPE: {gap_type}
DESCRIPTION: {description}
EVIDENCE OF GAP: {evidence}
SUGGESTED TOOL NAME: {suggested_name or 'auto-generate'}

CRITICAL REQUIREMENTS:
1. Keep the tool SIMPLE and FOCUSED - under 100 lines if possible
2. The tool MUST be syntactically valid Python that runs without errors
3. Include a simple test function that demonstrates usage
4. Close ALL brackets, parentheses, and quotes
5. Do NOT generate overly complex tools - simple and working beats complex and broken

For verification gaps: Just check constraints computationally, don't overthink it
For reasoning gaps: Simple step-by-step externalization
For computation gaps: Show work, verify results

Output ONLY valid Python code. Start with #!/usr/bin/env python3
End with if __name__ == "__main__": and a simple test call.
VERIFY YOUR CODE IS COMPLETE BEFORE OUTPUTTING."""

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",  # Use Sonnet for speed
            max_tokens=3000,  # Increased for complete code
            temperature=0.2,  # Lower temp for more reliable code
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.content[0].text

        # Clean up code if needed
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.strip()

        # Generate file name
        name = suggested_name or f"auto_{gap_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        name = name.replace("-", "_").replace(" ", "_").lower()
        file_path = TOOLS_DIR / f"{name}.py"

        return code, str(file_path)

    def _generate_from_template(
        self,
        gap_type: str,
        description: str,
        suggested_name: Optional[str]
    ) -> Tuple[str, str]:
        """Fallback template-based generation."""
        template = TOOL_TEMPLATES.get(gap_type, TOOL_TEMPLATES["reasoning"])
        name = suggested_name or f"auto_{gap_type}"
        name = name.replace("-", "_").replace(" ", "_").lower()

        code = f'''#!/usr/bin/env python3
"""
Auto-generated tool: {name}
Purpose: {description}
Generated: {datetime.now().isoformat()}
"""

{template.format(name=name, description=description)}

def test_{name}():
    """Test the generated tool."""
    # Add test cases here
    print("Test not implemented - add test cases")

if __name__ == "__main__":
    test_{name}()
'''

        file_path = TOOLS_DIR / f"{name}.py"
        return code, str(file_path)

    def validate_tool(self, code: str) -> Tuple[bool, str]:
        """Validate generated code by attempting to run it."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            # Try to compile
            result = subprocess.run(
                ['python3', '-m', 'py_compile', temp_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False, f"Syntax error: {result.stderr}"

            # Try to run (with timeout)
            result = subprocess.run(
                ['python3', temp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                return False, f"Runtime error: {result.stderr}"

            return True, f"Success: {result.stdout[:500]}"

        except subprocess.TimeoutExpired:
            return False, "Timeout during validation"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def generate_and_save(
        self,
        gap_type: str,
        description: str,
        evidence: str,
        suggested_name: Optional[str] = None,
        max_retries: int = 2
    ) -> GeneratedTool:
        """Generate, validate, and save a tool. Retry on syntax errors."""

        for attempt in range(max_retries + 1):
            code, file_path = self.generate_from_gap(
                gap_type, description, evidence, suggested_name
            )

            # Validate
            valid, validation_msg = self.validate_tool(code)

            if valid:
                # Save the tool
                Path(file_path).write_text(code)
                print(f"✓ Tool saved to {file_path}")
                break
            else:
                if attempt < max_retries and "Syntax error" in validation_msg:
                    print(f"  Attempt {attempt + 1} failed, retrying...")
                    continue
                print(f"✗ Validation failed: {validation_msg}")
                # Still record the attempt
                file_path = file_path + ".failed"
                break

        tool = GeneratedTool(
            name=Path(file_path).stem,
            purpose=description,
            code=code,
            file_path=file_path,
            generated_at=datetime.now().isoformat(),
            from_gap=f"{gap_type}: {description}",
            validated=valid,
            validation_result=validation_msg
        )

        self.generated.append({
            "name": tool.name,
            "purpose": tool.purpose,
            "file_path": tool.file_path,
            "generated_at": tool.generated_at,
            "validated": tool.validated,
            "validation_result": tool.validation_result
        })
        self._save_history()

        return tool


def demo_generation():
    """Demo the tool generator."""
    generator = ToolGenerator()

    print("=== TOOL GENERATOR DEMO ===\n")

    # Demo with template (no API key needed)
    print("Generating from template...")
    code, path = generator._generate_from_template(
        gap_type="verification",
        description="Check if a proposed solution satisfies constraints",
        suggested_name="constraint_checker"
    )
    print(f"Generated {len(code)} chars of code")
    print(f"Would save to: {path}")

    # Show first 500 chars
    print("\nFirst 500 chars of generated code:")
    print("-" * 40)
    print(code[:500])


if __name__ == "__main__":
    demo_generation()
