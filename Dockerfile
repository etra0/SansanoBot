FROM python:3.7-slim

WORKDIR /sansanobot

COPY . /sansanobot

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "main.py"]
