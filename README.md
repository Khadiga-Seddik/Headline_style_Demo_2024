# How to publish and set up the dockerzed application

## Prerequisites

- Docker installed on your local machine and server
- Access to a private Docker repository (e.g., Docker Hub, AWS ECR, or another registry)
- Docker Compose installed on both local machine and server

## How to get the project onto the server (These steps should be done in the locally on your terminal. NOT ON THE SERVER!)

`docker login`

`docker-compose build`

`docker tag survey-web:latest andersbremnes/newsrecsurvey:latest`

`docker push andersbremnes/newsrecsurvey:latest`

### Step 2: Pull Docker Image from Private Repository on the Server (These steps should be done on the server!)

    Log in to your docker account on the server

`docker login`

Go to the app folder:
`cd app`

    Use this docker-compose command to pull the images

`docker-compose pull`

## How to set up the dockerized application

**Step 1**
run the command `sudo docker-compose up`
For production server you can run `sudo docker-compose up -d` to avoid terminal log

**Step 2**
Create a superuser so you can access the database by running the following command:
`sudo docker-compose exec web python manage.py createsuperuser`
And follow the instructions.

**Step 3**
To populate the database do the following commands:
`sudo docker-compose exec web python manage.py load_data2 data/baseline.csv`

# How to run locally through django

1. Go to the settings.py file in the "NEWSREC_survey folder and do the following:

- Make sure the correct allowed hosts is set
- There are some database settings which are commented out which is used for django applicatio running. Comment this in
- Comment out the database settings that are related to the dockerized application. Both these steps are marked with a comment

2. Then load the datasets into the databse please follow the below instructions:

- From the root folder of the project run the following command:
  `python manage.py load_data2 data/baseline.csv`

3. Create a superuser to be able to enter the /admin page

- Run the following command from the root folder:
  `python manage.py createsuperuser`
- And follow the steps in the terminal
