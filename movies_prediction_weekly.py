import pandas as pd
import numpy as np
import hopsworks
import joblib
import os
from src import helpers



def predict_movie_revenue():
    api_key = os.getenv("HOPSWORKS_KEY")
    print(api_key)
    project = hopsworks.login(api_key_value=api_key)
    fs = project.get_feature_store()
    # Retrieve feature groups
    movies_fg = fs.get_feature_group(
        name='raw_movies_info', 
        version=3,
    )
    print(movies_fg.show(5))


    movie_features = helpers.get_upcoming_movies_list()
    batch_data = pd.get_dummies(movie_features, columns=['star_present'])
    features = ['budget', 'popularity','cast_popularity', 'crew_popularity', 'star_present_no','star_present_yes']
    batch_data = batch_data[features]
    batch_data['budget'] = np.log1p(batch_data['budget'])


   
    mr = project.get_model_registry()
    # Retrieve the model from the model registry
    retrieved_model = mr.get_model(
    name="random_forest_revenue_prediction_model",
    version=1
    )
    # Download the saved model files to a local directory
    saved_model_dir = retrieved_model.download()

    print('download')

    model = joblib.load(saved_model_dir + "/random_forest_revenue_prediction.pkl")
    
    print('done!')

    y_pred = model.predict(batch_data)
    
    print('Details of the film :')
    print(movie_features)
    print()

    print(f'Predicted box office score : {np.expm1(y_pred)}')
    print()

    movie_features['revenue'] = np.expm1(y_pred)

    print(movie_features.info())
    movie_features['revenue'] = movie_features['revenue'].astype(int) 
    print(movie_features.info())
    movies_fg.insert(movie_features, write_options={"wait_for_job" : False})


if __name__ == "__main__":
    predict_movie_revenue()