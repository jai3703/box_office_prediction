import pandas as pd
import pickle
import requests
import json
import numpy as np
from dotenv import load_dotenv
import os
from datetime import date , timedelta
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


def get_upcoming_movies_list()->pd.DataFrame:
    today_date = date.today()
    next_week_date = today_date + timedelta(days=7)
    url = (f"""https://api.themoviedb.org/3/discover/movie?api_key={api_key}&include_adult=false&include_video=false&page=1&"""
        f"""release_date.gte={str(today_date)}&release_date.lte={str(next_week_date)}&"""
            f"""sort_by=revenue.desc&with_original_language=hi&with_release_type=2|3""")
    response = requests.get(url).json()
    upcoming_release =pd.DataFrame(response['results'])
    movie_details = pd.DataFrame()
    for i in range(len(upcoming_release)):
        movie_details= pd.concat([movie_details,
                              pd.DataFrame([get_features_movie(upcoming_release['id'][i])]
                                           )])
    movie_details = movie_details[movie_details['budget']>0].reset_index(drop=True)
    #movie_details = movie_details.drop('revenue',axis=1)
    return movie_details
    


