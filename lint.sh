black saltapi tests && \
isort saltapi tests && \
flake8 --ignore-extend=S saltapi tests && \
mypy saltapi && \
pytest
