FROM ubuntu:18.04

RUN apt-get update && apt-get -y install python3-pip ffmpeg

WORKDIR /home/deelhetmee/

COPY . /home/deelhetmee

RUN pip3 install -r requirements.txt

CMD ["python3", "webserver.py"]