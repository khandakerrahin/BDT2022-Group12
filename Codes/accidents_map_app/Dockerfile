# Dockerfile, Image, Container
FROM python:3.9

RUN apt-get update -y
WORKDIR /webapp
COPY . .
RUN pip install flask

ENTRYPOINT [ "python" ]
CMD ["webapp.py" ]