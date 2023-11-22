FROM ubuntu:focal
MAINTAINER YuWang nottwya@gmail.com

RUN apt-get update \
    && apt-get install -y python3 \
    && apt-get install -y  perl python3-pip \
    && pip3 install Flask pymysql \
    && DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai apt-get -y install tzdata \
    && apt-get install -y mysql-server \
    && pip3 install tensorflow==2.3.1 \
    && apt-get install -y vcftools
