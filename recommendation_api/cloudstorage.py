import json
import pickle

import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from google.cloud import storage


class GoogleCloudStorage:
    '''
    Google Cloud Storage操作に関するクラス
    Google Cloud StorageのデータをダウンロードしてPythonのデータ型に変換する
    Pythonのデータ型をアップロードしてGoogle Cloud Storageのデータに変換する
    '''
    def __init__(self, parameter: dict):
        """
        同一プロジェクト内のバケットのみ必要なので、デフォルトAppEngineサービスアカウントの
        認証情報でクラウドストレージに接続する
        """
        self.__bucket_name = parameter['bucket_name']
        self.__storage_client = storage.Client()

    def list_blobs(self, prefix: str, delim: str=None):
        """Lists all the blobs in the bucket that begin with the prefix.

        See: https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python

        This can be used to list all blobs in a "folder", e.g. "public/".

        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:

            a/1.txt
            a/b/2.txt

        If you just specify prefix = 'a', you'll get back:

            a/1.txt
            a/b/2.txt

        However, if you specify prefix='a' and delimiter='/', you'll get back:

            a/1.txt

        Additionally, the same request will return blobs.prefixes populated with:

            a/b/
        """
        blobs = list(self.__storage_client.list_blobs(
            self.__bucket_name, prefix=prefix, delimiter=delim
        ))
        return blobs


class Doc2VecModel(GoogleCloudStorage):
    def __init__(self, parameter: dict):
        super().__init__(parameter)
        self.__model = None
    
    def load_model(self) -> Doc2Vec:
        blobs = self.list_blobs(prefix='trained')
        if len(blobs) == 0:
            print('failed to load model.')
            return None
        
        model_blob = blobs[0]
        print('loaded model. name: {}'.format(model_blob.name))
        self.__model = pickle.loads(model_blob.download_as_string())
        return self.__model

    def model_exists(self) -> bool:
        return (self.__model is not None)


class UsersTbl(GoogleCloudStorage):
    def __init__(self, parameter: dict):
        super(UsersTbl, self).__init__(parameter)
        self.__tbl = None
    
    def load_tbl(self) -> pd.DataFrame:
        blobs = self.list_blobs(prefix='users')
        if len(blobs) == 0:
            print('failed to load users table.')
            return None
        
        tbl_blob = blobs[0]
        print('loaded tbl. name: {}'.format(tbl_blob.name))
        self.__tbl = pickle.loads(tbl_blob.download_as_string())
        return self.__tbl

    def tbl_exists(self) -> bool:
        return (self.__tbl is not None)


class UserVectors(GoogleCloudStorage):
    def __init__(self, parameter: dict):
        super(UserVectors, self).__init__(parameter)
        self.__vectors = []
    
    def load_vectors(self) -> list:
        vector_blobs = self.list_blobs(prefix='vectors')
        if len(vector_blobs) == 0:
            print('failed to load user vectors.')
            return None

        for vector_blob in vector_blobs:
            # vectors/XXXXXXXXX.json => XXXXXXXXX
            vector_uuid = vector_blob.name[8:-5]
            vector_value = json.loads(vector_blob.download_as_string())
            self.__vectors.append({'user_id': vector_uuid, 'vector': vector_value})
        print('loaded vectors (len: {})'.format(len(self.__vectors)))
        return self.__vectors
    
    def vectors_exist(self) -> bool:
        return (len(self.__vectors) != 0)
