# 
This repository contains a docker file which is to reproduce the docker that setup an environment for getting real time soccer premier league table. The docker image will install required dependencies and get the required library to get soccer data. It'll run the program and store the table in a file on every run.

# Usage

    docker build -t stable .
    docker run stable
