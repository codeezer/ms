
# Docker Reproducibility

This repository contains a docker file which is to reproduce the docker that setup an environment for getting real time soccer premier league table. The docker image will install required dependencies and get the required library to get soccer data. It'll run the program and store the table in a file on every run.

### Dockerfile Description

Specifies the OS to use
```
FROM ubuntu:18.04
```
Run the ubuntu application update
```
RUN apt-get update
```
Install the git and python package manager
```
RUN apt-get install -y git python3-pip 
```
Clone a program which gives the soccer league tables and score
```
RUN cd ~/ && git clone https://github.com/codeezer/
```
Go to the program directory and get latest league table and store it on file
```
RUN ~/livescore-cli/livescore.py -t bpl >> ~/latest_table.txt
```

### Usage

Build the docker file
```
docker build -t stable .
```
Run the built docker image and open a shell to the container
```
docker run -i -t stable
```
Get the content of the file on the container
```
cd && cat latest_table.txt
```
