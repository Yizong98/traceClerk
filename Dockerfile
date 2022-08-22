# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.7-buster

WORKDIR /

COPY ./clerk ./clerk
COPY ./setup.py .

# Builds production wheel file and removes source code.
RUN python setup.py bdist_wheel && rm -rf clerk && pip install ./dist/clerk-1.0.0-py3-none-any.whl

CMD [ "waitress-serve", "--port=5939" , "--call", "clerk:create_app"]