# Weather API

## Overview

This is a simple Rest API fetching weather information of a specified city written in Python.
This API is using a DARK SKY api to obtain weather informaiton, so you need to get one.

## Prerequisites

* DARK SKY API Key

## Required Python Libraries

* Flask 1.1.2
* geopy 1.22.0
* requests 2.23.0

## Usage

While app.py is running, simply access the url with location where you want to know weather info

For example:
* Access http://localhost:5000/location
* The following json is returned as a result

    {
        "location":"location",
        "temp_max":"Max Temperature ",
        "temp_min":"Min Temperature",
        "weather":"Sunny throughout the day."
    }

## Examples

### 1. Run locally using Docker container

You can test this API locally by running a docker container. 

    # use an official python container
    ## '-it': connect the docker container through a pseudo tty
    ## '-v $(pwd):/app': bind mount the current directory to /app in the container
    ## '-w /app': specify /app as the current working directory
    ## 'python': container image name
    ## '/bin/bash': run bash when accessing the container
    docker run -it --rm -v $(pwd):/app -w /app python /bin/bash

    # export dark sky api key
    export DARK_SKY_API_KEY=YourDarkSkyApiKey

    # install required Libraries
    pip install -r requirements.txt

    # run app.py
    python app.py

    # open another terminal and run curl with the following format
    ## curl http://localhost:5000/city_name
    ## port 5000 (default port used by flask)
    curl http://localhost:5000/tokyo

    # output
    #{"location":"Tokyo, Japan","temp_max":"81.04\u00b0F","temp_min":"61.79\u00b0F","weather":"Mostly cloudy throughout the day."}

### 2. Run on heroku

To deploy this api on heroku, you need to either create a heroku account or have a heroku account already.
Also, you need to install heroku cli to have the following work properly.
For more details, please go to heroku's documentation about deploying a python app.

    # initialize git inside the directory
    git init 
    # add files and commit them to git
    git add .
    git commit -m 'first commit
    
    # create heroku app
    heroku create myweatherapi
    
    # add Dark Sky API key to the heroku app on web browser(settings -> config vars)
    
    # push the git repo to heroku app
    git push heroku master

    # query the target url with curl
    curl https://myweatherapi.herokuapp.com/london                                   (git)-[master]
    
    #output
    #{"location":"London, Greater London, England, SW1A 2DX, United Kingdom","temp_max":"69.86\u00b0F","temp_min":"47.03\u00b0F","weather":"Mostly cloudy throughout the day."}

## Note

Apparently Dark Sky API will terminate its service at the end of 2021.
It seems that they have already stopped accepting new registrations, so unfortunately this API can only be used by those who already have the API key.
I may change the source to obtain weather info, but for now it remains as it. 
