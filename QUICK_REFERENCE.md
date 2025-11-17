# Claude Code Quick Reference

## Common Commands to Try

### Code Development
```
"Create a Python script that [does X]"
"Add a function to calculate [Y]"
"Refactor this code to be more efficient"
"Add error handling to the login function"
"Convert this JavaScript to TypeScript"
```

### Analysis & Understanding
```
"Explain what this code does"
"Show me the structure of this project"
"Find all functions that use database queries"
"Where is the authentication logic?"
"Analyze the performance of this algorithm"
```

### Testing
```
"Write unit tests for calculator.py"
"Run the test suite"
"Add test coverage for edge cases"
"Create integration tests for the API"
"Fix the failing tests"
```

### Git Operations
```
"Show git status"
"Commit these changes with message: [message]"
"Create a branch called feature/new-api"
"Show the diff for the last commit"
"Push to the remote repository"
```

### Debugging
```
"This function returns None, why?"
"Debug this error: [paste error]"
"Why is my loop infinite?"
"Fix the type errors in this file"
"Profile this code for performance issues"
```

### File Operations
```
"Find all Python files in src/"
"Search for 'TODO' comments"
"Read config.json and explain it"
"Create a new directory structure for a REST API"
"Show me all files modified in the last commit"
```

### Package Management
```
"Install pytest using pip"
"Add express to package.json"
"Update all npm dependencies"
"Create a requirements.txt file"
"Install dependencies from package.json"
```

### Documentation
```
"Add docstrings to all functions in this file"
"Create a README for this project"
"Generate API documentation"
"Add inline comments explaining this algorithm"
"Create a CONTRIBUTING.md guide"
```

### Web Research
```
"Search for the latest React best practices"
"How do I implement JWT authentication in Flask?"
"Fetch the documentation for FastAPI"
"What's the current stable version of Node.js?"
```

## Useful Patterns

### Multi-Step Tasks
```
"I want to create a REST API with user authentication:
1. Set up Flask project structure
2. Add user model and database
3. Implement JWT authentication
4. Create CRUD endpoints
5. Add tests
6. Document the API"
```

### Code Review
```
"Review this code and suggest improvements:
- Security issues
- Performance problems
- Best practices
- Code style"
```

### Learning
```
"Teach me about [concept] by showing example code"
"What's the difference between [A] and [B]?"
"Show me how to implement [pattern] in Python"
```

## Files Created for You

1. **claude_env_explorer.py** - Interactive tool to explore this environment
   - Run: `python3 claude_env_explorer.py` (interactive menu)
   - Run: `python3 claude_env_explorer.py --all` (show everything)

2. **CLAUDE_CODE_GUIDE.md** - Comprehensive guide to Claude Code

3. **QUICK_REFERENCE.md** - This file! Quick command examples

4. **demo_project/** - Sample project demonstrating:
   - Python module (calculator.py)
   - Unit tests (test_calculator.py)
   - Node.js config (package.json)
   - Documentation (README.md)

## Try It Now!

Test the demo project:
```bash
cd demo_project
python3 calculator.py
```

Or just ask me:
- "Run the calculator demo"
- "Show me how the calculator tests work"
- "Add a power function to the calculator"

## Environment Info

- **Python**: 3.11.14
- **Node.js**: 22.21.1
- **Git**: 2.43.0
- **Platform**: Linux x86_64

## Remember

- I can work on multiple files at once
- I track complex tasks with todo lists
- I can search your entire codebase
- I can run tests and show you results
- I can explain any code I write
- I can help you learn as we build

**Just tell me what you want to build, fix, or understand!**
