FROM python:3.12.2-slim-bullseye
WORKDIR /app
EXPOSE 5555
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "run.py" ]