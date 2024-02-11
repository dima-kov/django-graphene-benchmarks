FROM python:3.11-slim as base

RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install pip --upgrade

WORKDIR /app

CMD ["uvicorn", "octopus.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

# graphene-django main version
FROM base as sync

COPY project/sync /app/

RUN pip install -r requirements.txt

# graphene-django PR version
FROM base as async

COPY project/async /app/

RUN pip install -r requirements.txt
