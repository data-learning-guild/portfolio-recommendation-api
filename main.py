# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Flask-RESTful: Doc
# https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing

# [START gae_python38_app]
from flask import Flask
from flask_restful import Resource, Api, reqparse


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
api = Api(app)

dammy_users = [
    {
        "name": 'やまだたろう',
        "uuid": 'URDDX224S',
        "score": 0.34
    },
    {
        "name": 'うえだじろう',
        "uuid": 'URDDX224S',
        "score": 0.45
    },
    {
        "name": 'さとうごろう',
        "uuid": 'URDDX224S',
        "score": 0.56
    },
    {
        "name": 'すずきたつろう',
        "uuid": 'URDDX224S',
        "score": 0.67
    },
    {
        "name": 'たけだしろう',
        "uuid": 'URDDX224S',
        "score": 0.78
    }
]

class User(Resource):
    def get(self):
        """Get users list
        """
        users = [x['name'] for x in dammy_users]
        return {'users': users}

class UserSearch(Resource):
        
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('kw', required=True, type=str)
        self.parser.add_argument('max', required=False, type=int, default=3)

    def get(self):
        """Get users those are interested in search_word.
            Arguments.
                search_word: -
                max_num: recommend user list max size
        """
        args = self.parser.parse_args()
        search_word = args.kw
        max_num = args.max
        sorted_dammy_list = sorted(dammy_users, key=lambda x: x['score'], reverse=True)
        shrinked_dammy_list = sorted_dammy_list[:max_num]

        # make response
        response = {
            "kw": search_word,
            "recommended_users": shrinked_dammy_list
        }
        return response

##
## Actually setup the Api resource routing here
##
api.add_resource(User, '/users')
api.add_resource(UserSearch, '/users/search')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
