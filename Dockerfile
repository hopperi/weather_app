FROM python:3.11-slim-bullseye AS base

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ARG ENV_FILE=.env
ENV FLASK_APP=app.py
EXPOSE 5000
ENTRYPOINT ["sh", "-c"]
CMD ["sleep 10 && python -m flask run --host=0.0.0.0 --port=5000"]