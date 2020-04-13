# Developer Manual

The file is intended to explain to a developer how to set up and run this website on their machine and on a remote server.



## Docker
In order to ease deployment as much as we could, we decided to use [Docker](www.docker.com) to build our application. Docker is a tool designed to allow users to run applications by using "containers" that will transition seamlessly to all platforms that can install and run it.

To run the application locally, first install Docker and run the following commands in the project's root directory:
`docker build -f Dockerfile.dev -t williwaller .`

Once the image is built, you can run the container with the following command:
`docker run -p 4000:5000 williwaller`

If you then open `127.0.0.1:4000` you should see the website up and running.

The argument `-p` binds the local port 4000 to the docker port 5000 (the one used by the container). This can be changed to suit your needs.




## Deployment
In order to run our application on a server - again it is simplest to use Docker. A Dockerfile has been provided.

On your server, push the project directory and, within the root folder, build and run the container using  `Dockerfile.prod` this time.

Some environment variables will first need to be set for the application to run correctly.

On UNIX Systems, this can be done by running the command:

 `export VARIABLE_NAME="VARIABLE_VALUE"`

You will need to set the `PORT` env variable to the port you want to use and, if you want to use another database other than the sqlite file provided, you will need to set the `DATABASE_URL` variable to the SQL database URL you want to use.




## Heroku
In order to deploy our application, we have decided to use Heroku. If you want to deploy this application to a new Heroku dyno, follow [these instructions](https://devcenter.heroku.com/articles/git) to set up a Heroku git repository in the root folder of the application. We have included a heroku.yml file. 

Therefore, if you simply push this repository, Heroku will build the application using docker and the production Dockerfile automatically.. 




## Python and virtualenv
If you are experienced with python, you might prefer to use a virtual environment rather than Docker to work on this application. In this case, activate your virtual environment and run `pip install -r requirements.txt` to install all the necessary packages.

For development purposes, you will need to set the `FLASK_SETTINGS` variable to `config.DevelopmentConfig` on top of the other two described above.

Once you are all set, run `gunicorn -c config.py "app:create_app()"` to run the application.

