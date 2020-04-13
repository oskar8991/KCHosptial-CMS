SEG Major Project

Project #: 4

Team name: WilliWaller

Team members: Oskar Ljungdell, Scott Anderson, David Azoulai, Artur Ganeev, Antoine Gosset, Victoria Hayes, Ivan Hristev, Layth Mehdi

Run instructions :

## Deployment - Docker

In order to run our application on a server - a Dockerfile has been provided.

To run the application locally, first install Docker and run the following commands in the project's root directory:
`docker build -f Dockerfile.dev -t williwaller `

Once the image is built, you can run the container with the following command:
`docekr run -p 6000:5000 williwaller`

If you then open `127.0.0.1:6000` you should see the website up and running.

The argument `-p` binds the local port 6000 to the docker port 5000 (the one used by the container). This can be changed to suit your needs.

On your server, push the project directory and, within the root folder, build and run the container using  `Dockerfile.prod` this time.

Some environment variables will first need to be set for the application to run correctly.

On UNIX Systems, this can be done by running the command:

 `export VARIABLE_NAME="VARIABLE_VALUE"`

You will need to set the `PORT` env variable to the port you want to use and, if you want to use another database other than the sqlite file provided, you will need to set the `DATABASE_URL` variable to the SQL database URL you want to use.

## Python and virtualenv
Make sure you have python 3 and virtualenv installed. Then navigate to project directory and activate your virtual environment and run `pip install -r requirements.txt` to install all the necessary packages.

For development purposes, you will need to set the `FLASK_SETTINGS` variable to `config.DevelopmentConfig` on top of the other two described above.

Once you are all set, run `gunicorn -c config.py "app:create_app()"` to run the application.

Additionally, you can view the website at: https://williwaller.herokuapp.com/


