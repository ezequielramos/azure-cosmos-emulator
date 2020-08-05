FROM python:3.7.5-stretch 

COPY . /root/azure-cosmos-emulator

RUN apt update

WORKDIR /root/azure-cosmos-emulator

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/python", "azure-cosmos-emulator.py"]
