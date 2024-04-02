import pandas as pd
import numpy as np
import hopsworks
import joblib

project = hopsworks.login()
fs = project.get_feature_store()
movie_fg = fs.get_feature_group(name="movies", version=2)
query = movie_fg.select(['id']).read()
print(query)
# def g():

#     project = hopsworks.login()
#     fs = project.get_feature_store()
#     movie_fg = fs.get_feature_group(name="movie_predictions", version=1)
#     query = movie_fg.select(['id']).read()

#     movie_features = utils.get_latest_not_infered(query)

#     if movie_features == -1:
#         raise ValueError('No more movies with known budget to infer on, using TMDB now playing API.')

#     features = ['top_cast_popularity', 'budget', 'crew_popularity', 'similar_revenues']
#     scaling_factor = 1000000

#     movie_df = pd.DataFrame([movie_features])
#     x = movie_df[features]
#     x[['budget', 'similar_revenues']] = x[['budget', 'similar_revenues']]/scaling_factor

#     mr = project.get_model_registry()
#     model = mr.get_model("movie_kn14", version=1)
#     model_dir = model.download()

#     print('download')

#     model = joblib.load(model_dir + "/k-neighbours14.pkl")
    
#     print('done!')

#     y_pred = model.predict(x)
    
#     print('Details of the film :')
#     print(movie_features)
#     print()

#     print(f'Predicted box office score : {y_pred}')
#     print()

#     x['revenue'] = y_pred[0][0]
#     x['id'] = movie_df['id']
#     x[['budget', 'revenue', 'similar_revenues']] *= scaling_factor
#     x[['budget', 'revenue']] = x[['budget', 'revenue']].astype('int')

#     movie_fg.insert(x, write_options={"wait_for_job" : False})


# if __name__ == "__main__":
#     g()