black saltapi tests && \
bandit -r saltapi && \
isort saltapi tests && \
flake8 saltapi tests && \
mypy saltapi && \
pytest
