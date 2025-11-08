Contributing

Thank you for contributing to this project. Please follow these guidelines.

1. Development setup

- Follow instructions in `PROJECT_DOCUMENTATION.md` to run the application locally.
- Use a virtual environment and install dependencies with `pip install -r requirements.txt`.

2. Branching and commits

- Create a feature branch from `main`: `git checkout -b feature/your-feature`.
- Write clear commit messages and open pull requests to `main`.

3. Tests and CI

- Add tests under `tests/` and make sure they pass locally using `pytest`.
- CI runs on push and pull requests and includes a smoke test and linter.

4. Security

- Do not commit secrets or credentials. Use `.env` and GitHub secrets.

5. Code style

- Follow standard Python style (PEP8). Use `ruff` or `flake8` to lint changes.
