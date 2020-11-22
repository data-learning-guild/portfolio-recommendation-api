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
# App Engine + Cloud Storage
# https://cloud.google.com/appengine/docs/standard/python3/using-cloud-storage?hl=ja
# App Engine + Cloud Storage (Sample)
# https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/app-engine-cloud-storage-sample
# https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/storage/appengine-client
#
# https://cloud.google.com/storage/docs/reference/libraries
# https://cloud.google.com/storage/docs/downloading-objects#storage-download-object-code-sample
# https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python

# [START gae_python38_app]
import json

from flask import Flask
from flask_restful import Api

from recommendation_api.resources import User, UserSearch

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
api = Api(app)


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
