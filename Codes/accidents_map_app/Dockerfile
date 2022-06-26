# Dockerfile, Image, Container
FROM python:3.9

RUN apt-get update -y
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /webapp
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["webapp.py" ]