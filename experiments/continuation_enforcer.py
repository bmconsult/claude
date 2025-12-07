#!/usr/bin/env python3
"""
Continuation Enforcer - Prevents premature session closure
Tracks task completion percentage and enforces continuation until truly complete
"""

class ContinuationEnforcer:
    def __init__(self, task_description: str, estimated_steps: int):
        """
        Initialize the continuation enforcer
        
        Args:
            task_description: What needs to be accomplished
            estimated_steps: Estimated number of steps to completion
        """
        self.task_description = task_description
        self.estimated_steps = estimated_steps
        self.completed_steps = 0
        self.checkpoints = []
        self.force_continue_threshold = 0.80  # 80% threshold
        
    def mark_step_complete(self, step_description: str) -> dict:
        """Mark a step as complete and check if we should continue"""
        self.completed_steps += 1
        self.checkpoints.append(step_description)
        
        completion_pct = self.completed_steps / self.estimated_steps
        
        result = {
            "completion_percentage": round(completion_pct * 100, 1),
            "completed_steps": self.completed_steps,
            "total_steps": self.estimated_steps,
            "can_close": completion_pct >= 1.0,
            "must_continue": completion_pct < self.force_continue_threshold,
            "in_danger_zone": 0.80 <= completion_pct < 1.0,
            "message": self._get_status_message(completion_pct)
        }
        
        return result
    
    def _get_status_message(self, completion_pct: float) -> str:
        """Generate appropriate status message"""
        if completion_pct >= 1.0:
            return "✓ Task complete - safe to close session"
        elif completion_pct >= self.force_continue_threshold:
            return "⚠ DANGER ZONE: Do NOT close yet - task incomplete!"
        else:
            return f"→ Continue working - {round((1-completion_pct)*100)}% remaining"
    
    def get_remaining_work(self) -> str:
        """Get summary of remaining work"""
        remaining = self.estimated_steps - self.completed_steps
        return f"{remaining} steps remaining out of {self.estimated_steps} total"
    
    def override_complete(self, reason: str) -> dict:
        """Force mark as complete with justification"""
        return {
            "completion_percentage": 100.0,
            "override": True,
            "reason": reason,
            "can_close": True,
            "message": f"✓ Marked complete: {reason}"
        }


def test_continuation_enforcer():
    """Test the continuation enforcer"""
    print("=== Continuation Enforcer Test ===\n")
    
    # Create enforcer for a 10-step task
    enforcer = ContinuationEnforcer("Build complete Python tool", estimated_steps=10)
    
    print(f"Task: {enforcer.task_description}")
    print(f"Estimated steps: {enforcer.estimated_steps}\n")
    
    # Simulate completing steps
    steps = [
        "Define requirements",
        "Create class structure",
        "Implement core logic",
        "Add error handling",
        "Write documentation",
        "Create test function",
        "Test basic functionality",
        "Test edge cases"
    ]
    
    for step in steps:
        result = enforcer.mark_step_complete(step)
        print(f"Step {result['completed_steps']}: {step}")
        print(f"  Progress: {result['completion_percentage']}%")
        print(f"  Status: {result['message']}")
        
        if result['in_danger_zone']:
            print("  ⚠⚠⚠ ALERT: Entering premature closure zone! ⚠⚠⚠")
        
        print()
    
    print(f"\nRemaining: {enforcer.get_remaining_work()}")
    
    # Complete final steps
    print("\n--- Completing final steps ---\n")
    for step in ["Verify all code", "Final review"]:
        result = enforcer.mark_step_complete(step)
        print(f"Step {result['completed_steps']}: {step}")
        print(f"  Progress: {result['completion_percentage']}%")
        print(f"  Status: {result['message']}")
        print(f"  Can close: {result['can_close']}")
        print()


if __name__ == "__main__":
    test_continuation_enforcer()