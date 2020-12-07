FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y git python3-pip 
RUN cd ~/ && git clone https://github.com/bannsec/pySym.git && cd pySym
RUN pySym/bin/activate
RUN pip install .
