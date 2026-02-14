# EDMS Starter Kit (Beginner Friendly)

You asked to **start from scratch**. This repository is now a small, clean Python starter you can learn step by step.

## What this project does
This is a tiny EDMS (Electronic Document Management System) example that supports:
- creating a document
- moving it through workflow states (`draft -> review -> approved`)
- checking simple role permissions
- saving an audit trail

It is intentionally small so you can understand every file.

## Project structure
- `edms/models.py` → data structures (users, documents, workflow states)
- `edms/system.py` → main business logic
- `tests/test_system.py` → tests (good examples to learn from)

## 1) Setup
You only need Python 3.10+.

## 2) Run tests
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

If tests are all green, your system is working.

## 3) First learning steps
1. Open `edms/models.py` and read the enums and dataclasses.
2. Open `edms/system.py` and read one method at a time.
3. Open `tests/test_system.py` and match each test to methods in `system.py`.
4. Make one tiny change (example: new workflow comment) and rerun tests.

## 4) What to build next
When you're ready, we can add features one by one:
- document versioning (`v1.0`, `v1.1`)
- electronic signatures
- controlled printing
- reports and filters

If you want, I can guide you in a strict beginner mode with very small tasks.
