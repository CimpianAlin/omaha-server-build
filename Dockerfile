FROM python:3

WORKDIR /src

COPY requirements.txt.lock ./
RUN pip install --no-cache-dir -r requirements.txt.lock
RUN apt-get update && apt-get install -y zip

CMD [ "bash", "-l" ]
