FROM microsoft/azure-cli

LABEL Name=az_dialog Version=0.0.1

WORKDIR /app
ADD . /app

RUN apk update \
    && apk add dialog python3 py3-dialog py3-pip dialog

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "-m", "az_dialog"]
