FROM  python:latest

# base image installs
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends \
build-essential gcc -y
RUN apt-get install iputils-ping -y
RUN apt-get install iperf3 -y


#virtenv initial setup
WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY . .
COPY requirements.txt .
RUN pip install --upgrade pip

ENV PATH="/usr/app/venv/bin:$PATH"
ENV port 888


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 888
CMD ["python","iperf_server.py"]