FROM python:3.11-slim

RUN pip install --no-cache-dir ansible-core

RUN ansible-galaxy collection install cisco.ios

ENV username cian
RUN echo cian

WORKDIR /ansible