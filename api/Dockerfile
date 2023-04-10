FROM python:3.10 as python
ENV PYTHONUNBUFFERED=true
WORKDIR /api


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./poetry.lock /api/poetry.lock
COPY ./pyproject.toml /api/pyproject.toml
COPY ./README.md /api/README.md
COPY ./src /api/src
RUN poetry install --no-interaction --no-ansi -vvv



FROM python as runtime
ENV PATH="/api/.venv/bin:$PATH"
WORKDIR /
COPY --from=poetry /api /api
EXPOSE 8000
CMD ["uvicorn", "api.src.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]