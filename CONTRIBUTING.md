# Contributing Guidelines
Thank you for considering contributing to **EventFlow**.

We welcome improvements, bug fixes, and new features.

## 📌 How to Contribute
1. Fork the repo and create your branch
```bash
git checkout -b feature/my-new-feature
```

2. Commit your changes with a clear message. e.g
```bash
git commit -m "feat: add postgres checkpoint integration"
```

3. Push to your fork and submit a Pull Request

## 🛠 Development Environment
We recommend the following setup for contributors to ensure consistency and code quality:
- **IDE**: Visual Studio Code (VS Code) is the recommended IDE.
- Required VS Code Extensions:
    - **Python** – official Python support.
    - **Pylance** – fast type checking and autocompletion.
    - **Mypy Type Checker** – static type checking.
    - **Isort** – import sorting.
    - **Ruff** – linter and code formatter.

## 🧑‍💻 Coding Standards

- Follow **PEP8** style guide for Python. (You can use a linter like **ruff**)
- Use snake_case for file names and functions.
- Write docstrings for functions and classes.
- Keep modules small and focused (separation of concerns).
- Before committing, ensure:
    - Imports are sorted with isort.
    - Code passes lint checks with ruff.
    - Type checking passes with mypy.

## 🧪 Tests
- Add or update tests for any change in app/tests/.
- Ensure all tests pass before submitting a PR.

## 📄 Commit Message Convention
- **feat**: – new feature
- **fix**: – bug fix
- **docs**: – documentation only changes
- **refactor**: – code restructuring without behavior change
- **test**: – adding or updating tests
- **chore**: – maintenance tasks
