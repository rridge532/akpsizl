# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7.2

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /akpsi

ADD ./requirement.txt /akpsi/

RUN pip install -r /akpsi/requirement.txt

RUN mkdir /src;

WORKDIR /src
