FROM python:3.10
#setup
WORKDIR /code/app

# RUN apt-get install -y python3-venv
# RUN apt-get install -y python3-dev
RUN python3.10 -m venv venv
RUN . venv/bin/activate

ENV PYTHON_VENV=/code/app/venv/bin/python3

# Load requirements files
# COPY requirements.in /code/app/requirements.in
COPY requirements.txt /code/app/requirements.txt


RUN ${PYTHON_VENV} -m pip install -U --quiet pip==22.1
# RUN ${PYTHON_VENV} -m pip install pip-tools

# RUN ${PYTHON_VENV} -m piptools compile --quiet --output-file /code/app/requirements.txt /code/app/requirements.in
RUN ${PYTHON_VENV} -m pip install -r /code/app/requirements.txt

COPY .env /code/app/.env

# Build back end / fastapi / server
WORKDIR /code/app


ENTRYPOINT ${PYTHON_VENV} -m uvicorn --factory app.entrypoints.http_server:app_factory  --log-level debug --reload --host 0.0.0.0 --port 8080