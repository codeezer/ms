FROM centos:8
RUN yum -y install git pip
RUN cd /root/ && git clone github.com/codeezer/livescore-cli
RUN cd /root/livescore-cli
RUN ./setup
CMD livescore -t bpl >> latest_table.txt
