FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN apt update --fix-missing && apt upgrade -y
RUN apt install -y make \
                   gcc \
                   libpq-dev \
                   libffi-dev \
                   libssl-dev \
                   libcurl4-openssl-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]