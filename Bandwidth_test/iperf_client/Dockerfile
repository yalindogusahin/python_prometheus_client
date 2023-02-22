FROM  python

# base image installs
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc 
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
ENV hostName 8.8.8.8
ENV port 5202
ENV schedule_time 900

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5201 8080
CMD ["python","main.py"]