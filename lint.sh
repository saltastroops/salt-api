black saltapi tests --preview && \
isort saltapi tests && \
flake8 saltapi tests && \
mypy saltapi && \
pytest
