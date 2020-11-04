FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y git python3-pip 
RUN cd ~/ && git clone https://github.com/codeezer/livescore-cli && cd ~/livescore-cli && ./setup
RUN ~/livescore-cli/livescore.py -t bpl >> ~/latest_table.txt
CMD ~/livescore-cli/livescore.py -t bpl >> ~/latest_table.txt
