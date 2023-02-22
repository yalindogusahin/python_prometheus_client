# Python prometheus client

You need to change hostname in main.py then you good to go.

The project basically pings to the host and exports metrics exposed to port 8080 of localhost.

Run command below:

        pip install -r requirements.txt

        python main.py

To see the metrics you can enter localhost:8080 to your browser or use cli

        curl localhost:8080

# Docker Build

If you want to use application in container you just need to run the command below. (Don't forget to change your app name)

        docker build -t yourappname .

        docker run -it --expose 8080 -p 8080:8080 yourappname
