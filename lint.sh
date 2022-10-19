poetry run black saltapi tests && \
poetry run bandit -r saltapi && \
poetry run isort saltapi tests && \
poetry run flake8 saltapi tests && \
poetry run mypy saltapi && \
poetry run pytest
