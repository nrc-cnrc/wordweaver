# Base Image
FROM ubuntu:latest

# Set environment variables. These must point to actual folders on the machine you build the docker image with.
ARG config_dir=/path/to/configs
ARG data_dir=/path/to/data

ENV DEBIAN_FRONTEND=noninteractive

# Copy files
COPY . wordweaver/
RUN mkdir /configs
RUN mkdir /data
COPY $config_dir /configs
COPY $data_dir /data
ENV CONFIG_DIR=/configs
ENV DATA_DIR=/data

# get dependencies
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt-get install -y nano
RUN apt-get install -y subversion flex bison libreadline-dev libz-dev
RUN apt-get install -y git-all
RUN pip3 install -r wordweaver/requirements.txt
RUN git clone https://github.com/eddieantonio/foma.git
RUN cd foma/foma && make && make install
RUN cd /wordweaver && pip3 install -e .

# Set workdir/entrypoint
WORKDIR /

CMD gunicorn wordweaver.app:app --bind 0.0.0.0:$PORT



