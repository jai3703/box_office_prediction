# Project : Box-office Revenue Prediction

**Owner**: Jai Kumar Pandey

## 1. Description

This project is a serverless ML pipeline that creates models for upcoming box office performance predictions of recently released bollywood films. The model is trained on well selected features of past films and solving a regression problem tries to infer on the revenue of new films. The datasource we chose is the [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started), an online API giving a free access to a good amount of film description, frequently updated, and with performant and interesting query possibilities. One can get the access via an online formula. 

The pipeline uses Hopsworks for efficient storage (features and models), Huggingface web app for user interface, and Github Actions for workflows.

## 2. Structure and details

### 2.1. Struture of the project 

At the center of the system is Hopsworks. It receives and stores the features created from helpers.py, s interacts with workflows and with Huggingface. The offline dataset is fetched from TMDB API in the feature pipeline. Data is also fetched in the workflows for daily inference, and from Huggingface for details of movies.

This project involves different online services. In the code, we need API private keys to access Hopsworks and TMDB API. We added them as secret keys on Github for the workflows, and you will not have access to them on the repository. If you want to run this code, you should create your owns. 

For clarity, all functions basic functions and functions for feature extraction and TMDB API interactions are coded in *helpers.py* under src folder

### 2.2 Features selection and pipeline

TMDB API gives acces to details about the movies (a primary key id, budget of the film, revenues, released date, runtime, title, overview, genre tc...) and interesting pre-computed features (vote_average of the movie on their website and popularity). One can access similar movies, crew and casting wit additional queries. Based on that, we computed feature we found relevant :
* *crew_popularity* the sum of key peoples popularity in the movie crew (director, producer, production manager etc...)
* *cast_popularity* the sum of casting's polularity.

We scrapped movies from year 2000 to 2023. We only kept the one that had well defined features, especially budget and revenue for training. 

### 2.3 Workflows

There is one worksflow linked to Github actions :

* *movies_prediction_weekly.py* use the upcoming TMDB API to fetch the recent movies. It chooses a movie that is not yet in the feature group, predict his revenue and insert the new sample in the feature group. It runs on a weekly  basis.


### 2.4 HuggingFace app

One can find the user interface app [here](https://huggingface.co/spaces/Jai3703/box_office_prediction).

