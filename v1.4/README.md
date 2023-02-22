# Python prometheus client

You need to change hostname in main.py then you good to go.

The project basically pings to the selected host and exports metrics exposed to port 8080 of localhost.

Run command below:

        pip install -r requirements.txt

        python main.py

To see the metrics you can enter localhost:8080 to your browser or use cli

        curl localhost:8080

# Docker Build

If you want to use application in container you just need to run the command below. (Don't forget to change your app name)

        docker build -t yourappname .

There are 3 Environment variable of container. I've selected tcping service to 8.8.8.8 port 80. You can change those variables to your use case.

- hostName 8.8.8.8
- port 80
- mission tcping

        docker run -e hostName=github.com -e mission=tcping -e port=443 -it --expose 8080 -p 8080:8080 yourappname
