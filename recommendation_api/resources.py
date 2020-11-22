import os

import numpy as np
import pandas as pd
from flask_restful import Resource, reqparse
from gensim.models.doc2vec import Doc2Vec
from janome.tokenizer import Tokenizer

from recommendation_api.cloudstorage import Doc2VecModel
from recommendation_api.cloudstorage import UsersTbl
from recommendation_api.cloudstorage import UserVectors
from recommendation_api.preprocess import clean_msg


# initialize prediction
param = {'bucket_name': os.environ['CLOUD_STORAGE_BUCKET']}

model_storage = Doc2VecModel(param)
model = model_storage.load_model()

def user_info(param: dict) -> pd.DataFrame:
    """get user info
    """
    user_tbl_storage = UsersTbl(param)
    user_tbl = user_tbl_storage.load_tbl()

    user_vectors_storage = UserVectors(param)
    user_vectors = user_vectors_storage.load_vectors()

    df_user_vectors = pd.DataFrame(user_vectors)
    df_user_info = pd.merge(user_tbl, df_user_vectors, on='user_id', how='left')
    return df_user_info

user_db = user_info(param) # columns = ['user_id', 'name', 'vector']

# dammy_users = [
#     {
#         "name": 'やまだたろう',
#         "uuid": 'URDDX224S',
#         "score": 0.34
#     },
#     {
#         "name": 'うえだじろう',
#         "uuid": 'URDDX224S',
#         "score": 0.45
#     },
#     {
#         "name": 'さとうごろう',
#         "uuid": 'URDDX224S',
#         "score": 0.56
#     },
#     {
#         "name": 'すずきたつろう',
#         "uuid": 'URDDX224S',
#         "score": 0.67
#     },
#     {
#         "name": 'たけだしろう',
#         "uuid": 'URDDX224S',
#         "score": 0.78
#     }
# ]


class User(Resource):
    def get(self):
        """Get users list
        """
        users = user_db['name'].values.tolist()
        return {'users': users}

class UserSearch(Resource):
        
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('kw', required=True, type=str)
        self.parser.add_argument('max', required=False, type=int, default=3)
        self.t = Tokenizer()

    def cos_similarity(self, _x: list, _y: list) -> float:
        """cos similarity for small value
        """
        vx = np.array(_x) * 10000
        vy = np.array(_y) * 10000
        return np.dot(vx, vy) / (np.linalg.norm(vx) * np.linalg.norm(vy))

    def get(self):
        """Get users those are interested in search_word.
            Arguments.
                search_word: -
                max_num: recommend user list max size
        """
        # parse args
        args = self.parser.parse_args()
        search_word = args.kw
        max_num = args.max
        
        # vectorize keyword
        cleaned_ = clean_msg(search_word)
        cleaned_wkt = list(self.t.tokenize(cleaned_, wakati=True))
        key_vector = model.infer_vector(cleaned_wkt).tolist()
        
        # calc similarity scores
        scores = []
        for row in user_db.itertuples():
            score = self.cos_similarity(key_vector, row.vector)
            scores.append(score)
        user_db['score'] = scores

        # extract top users
        top_user_db = user_db.sort_values('score', ascending=False)[:max_num]

        # make response
        response = {
            "kw": search_word,
            "recommended_users": list(top_user_db.T.to_dict().values())
        }
        return response
