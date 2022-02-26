FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# install required packages
COPY requirements.txt ./requirements.txt

RUN \
pip3 install -U -r requirements.txt

# copy app files to container directory
COPY . ./

# add docker label
ARG TITLE
LABEL org.opencontainers.image.title=$TITLE

# add docker label
ARG BUILD_DATE
LABEL org.opencontainers.image.create=$BUILD_DATE

EXPOSE 80
CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
