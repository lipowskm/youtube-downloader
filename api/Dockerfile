FROM ubuntu:22.04 as python
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends ffmpeg
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10
ENV PYTHONUNBUFFERED=true
WORKDIR /api

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python3 -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python3 -
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
CMD ["uvicorn", "api.src.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]