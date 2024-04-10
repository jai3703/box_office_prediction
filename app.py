import gradio as gr
import os
import numpy as np
import datetime as dt
import hopsworks
import pandas as pd
from src import helpers
import random 
from PIL import Image
from io import BytesIO
import requests
import pickle

def get_new_predictions():
    api_key = os.getenv("HOPSWORKS_KEY")
    project = hopsworks.login(api_key_value=api_key)
    fs = project.get_feature_store()
    # Retrieve feature groups
    movies_fg = fs.get_feature_group(
        name='raw_movies_info', 
        version=3,
    )

    query = movies_fg.select_all()

    new_predictions_df = query.read()
    hopsworks.logout()

    MAX_MOVIES = 3

    new_predictions_df.sort_values(by = 'release_date', ascending = False, inplace = True)
    new_predictions_df = new_predictions_df.head(3)
    ids = new_predictions_df['id'].tolist()
    print(f"Predicted movies are {ids}")

    details = []
    for i, movie_id in enumerate(ids):

        movie_details = helpers.get_movie_details(movie_id)
        if movie_details['budget'] > 0 : 
            # movie_details['predicted_revenue'] = new_predictions[new_predictions['id'] == movie_id]['revenue'].values[0]
            movie_details['predicted_revenue'] = new_predictions_df.iloc[i,:]['revenue']

            # movie_details['release_date'] = dt.datetime.strptime(movie_details['release_date'], '%Y-%m-%d').date()
            details.append(movie_details)

    details = pd.DataFrame(details)
    details.sort_values(by = 'release_date', ascending = False, inplace = True)
  
    new_titles = [f"### {title}" for title in details['title']]
    new_revenues =  [f"#### Predicted revenue is {int(revenue)}\$" for revenue in details['predicted_revenue']]

    get_img = lambda poster_path : Image.open(BytesIO(requests.get(f"https://image.tmdb.org/t/p/w500{poster_path}", stream=True).content))
    new_images = [get_img(poster_path) for poster_path in details['poster_path']]
   
    return new_titles[0], new_titles[1], new_titles[2], new_revenues[0], new_revenues[1], new_revenues[2], new_images[0], new_images[1], new_images[2]


new_data = get_new_predictions()

with gr.Blocks("soft") as demo: 
    live = True
    gr.Markdown("## Movie revenue prediction")
    with gr.Tabs():
        with gr.TabItem("New movies"):
            gr.Markdown("# Prediction for recently released movies")
            gr.Markdown("Press the button to see other new predictions!")
            reload_button = gr.Button(value="Refresh")
            with gr.Row():
                title_0 = gr.Markdown(new_data[0])
                title_1 = gr.Markdown(new_data[1])
                title_2 = gr.Markdown(new_data[2])
            with gr.Row():
                image_0 = gr.Image(new_data[6])
                image_1 = gr.Image(new_data[7])
                image_2 = gr.Image(new_data[8])
            with gr.Row(): 
                prediction_0 = gr.Markdown(new_data[3])
                prediction_1 = gr.Markdown(new_data[4])
                prediction_2 = gr.Markdown(new_data[5])
        with gr.TabItem("Search a movie"): 
            gr.Markdown("## Predict a revenue for a selected movie! You can type the title you want to search for and we'll see if we can predict how much it will earn.")
                    
        #search_button.click(fn = fetch_prediction_for_title, inputs = [input_title], outputs = [prediction_s, image_search, budget, overview])
        reload_button.click(fn = get_new_predictions, inputs=[], outputs=[title_0, title_1, title_2, prediction_0, prediction_1, prediction_2, image_0, image_1, image_2])

demo.launch()