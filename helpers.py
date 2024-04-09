import pandas as pd
import pickle
import requests
import json
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_movie_details(movie_id:int)->dict: 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url).json()
    return response

def get_movie_credits(movie_id:int)->dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    response = requests.get(url).json()
    return response

def get_cast_crew_popularity(interest_area:str,movie_id:int)->float:
    cast_name =[]
    cast_details = get_movie_credits(movie_id)
    cast_popularity = 0
    for i in range(len(cast_details[interest_area])):
        if cast_details[interest_area][i]['name'] in cast_name:
            cast_popularity += 0
        else:
            cast_popularity += cast_details[interest_area][i]['popularity']
            cast_name.append(cast_details[interest_area][i]['name'])
    return cast_popularity


actors_star_power = {
    'Aamir Khan':[15480],
    'Salman Khan':[16045],
    'Shah Rukh Khan':[17705],
    'Akshay Kumar':[14730],
    'Ajay Devgn':[13760],
    'Hrithik Roshan':[12680],
    'Ranbir Kapoor':[5260]
}

def get_star_power(movie_id:int)->str:
    cast_details = get_movie_credits(movie_id)
    cast_names = []
    for i in range(len(cast_details['cast'])):
        cast_names.append(cast_details['cast'][i]['name'])
    count = 0
    for name in cast_names:
        if name in actors_star_power.keys():
            count+=1
        else:
            count +=0
    if count >=1:
        star_present = 'yes'
    else:
        star_present = 'no'
    return star_present


def get_features_movie(movie_id:int)->dict:
    useful_columns = ['budget','id','imdb_id','popularity','revenue','title','release_date']
    response = get_movie_details(movie_id)
    for key in list(response.keys()):
        if key not in useful_columns:
            del response[key]

    response['cast_popularity'] = get_cast_crew_popularity('cast',movie_id)
    response['crew_popularity'] = get_cast_crew_popularity('crew',movie_id)
    response['star_present'] = get_star_power(movie_id)
    return response
    