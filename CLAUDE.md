# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

django-followit is a reusable Django app that lets users follow instances of any Django model via the ContentTypes framework. It stores follow relationships in a single `FollowRecord` model and dynamically patches the User model at registration time.

Version 0.7.x requires Django 4.2 and supports Python 3.12 and 3.13. The `__init__.py` enforces a hard version gate rejecting Django < 4.2 or >= 5.0.

## Running Tests

Create a virtual environment and install Django 4.2:

```bash
python -m venv env
source env/bin/activate
pip install "django>=4.2,<5.0"
```

Run the tests:

```bash
cd followit/tests/ && python runtests.py
```

To test with a specific Python version via pyenv (e.g. 3.12):

```bash
$(pyenv prefix 3.12.10)/bin/python -m venv env12
source env12/bin/activate
pip install "django>=4.2,<5.0"
cd followit/tests/ && python runtests.py
```

Tests use an in-memory SQLite database configured in `followit/tests/settings.py`.

## Architecture

### Registration & Monkey-Patching (`followit/__init__.py`)

`followit.register(Model)` is the core API. Call it in `AppConfig.ready()`. It:
1. Adds `Model.get_followers()` to the registered model
2. Adds `User.get_followed_<model_name>s()` to the User model
3. Adds `User.is_following(obj)` (once, shared across all registered models)
4. Adds `User.follow_<model_name>(obj)` and `User.unfollow_<model_name>(obj)`

All methods are created via closures that capture the model class. Registered models are tracked in the module-level `followit.REGISTRY` dict (keyed by model name string).

### Data Model (`followit/models.py`)

Single model `FollowRecord` with three fields: `user` (FK), `content_type` (FK to ContentType), `object_id` (PositiveIntegerField). Uses generic foreign key pattern without GenericForeignKey field—lookups go through ContentType manually.

### Views & URLs (`followit/views.py`, `followit/urls.py`)

Three AJAX-only POST endpoints: `follow/<model_name>/<object_id>/`, `unfollow/...`, `toggle-follow/...`. All return JSON. Views are decorated with `followit_ajax_view` (checks auth, AJAX, model registration) and `post_only`.

### Compatibility (`followit/compat.py`)

Provides `get_user_model()` and `USER_MODEL_CLASS_NAME` for custom user model support. `AUTH_USER_CLASS` setting (note: not `AUTH_USER_MODEL`) controls the FK target in `FollowRecord`.

## Key Patterns to Know

- The `REGISTRY` dict maps lowercase model names to model classes. Views look up models from this dict, so model names in URLs must match exactly.
- `followit.register()` is idempotent—re-registering the same model is a no-op.
- The test app (`followit/tests/`) registers `Car`, `Alligator`, and `User` models in its `AppConfig.ready()` to exercise the registration system.
