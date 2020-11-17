import io
import os
import pickle
import pandas
import google.auth
from pathlib import Path
from google.cloud import storage
from google.oauth2 import service_account
from typing import List, Set, Dict, Tuple, TypeVar

class GoogleCloudStorage():
    '''
    Google Cloud Storage操作に関するクラス
    Google Cloud StorageのデータをダウンロードしてPythonのデータ型に変換する
    Pythonのデータ型をアップロードしてGoogle Cloud Storageのデータに変換する
    '''
    def __init__(self, parameter: Dict) -> None:
        '''
        リモートのサーバ上で動作保証するため下記四種の方法で認証を通している
        '''
        self.project_name = parameter['project']
        self.bucket_name = parameter['bucket']
        self.file_name = parameter['folder']
        self.mime_type = parameter['mime_type']
        self.credential_path = parameter['credential_path']


        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.client = storage.Client(self.project_name).from_service_account_json(self.credentials)
        except Exception as e:
            print(e)

        try:
            self.credentials, _ = google.auth.default()
            self.client = storage.Client(project=self.project_name, credentials=self.credentials)
        except Exception as e:
            print(e)

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials, _ = google.auth.default()
            if self.credentials.requires_scopes:
                self.credentials = self.credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
            self.client = storage.Client(credentials=self.credentials)
        except Exception as e:
            print(e)

        try:
            credentials_path = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
            if self.credentials.requires_scopes:
                self.credentials = self.credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
            self.client = storage.Client(credentials=self.credentials)
        except Exception as e:
            print(e)


    def download_as_string(self) -> str:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        return blob.download_as_string()

    def download_as_pickle(self) -> str:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        return pickle.loads(blob.download_as_string())

    def download_to_file(self, file_obj) -> object:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket) 
        return blob.download_to_file(file_obj)

    def upload_from_string(self, context: str) -> None:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_string(context, content_type=self.mime_type)

    def upload_from_ndjson(self, dataframe: pandas.core.frame.DataFrame) -> None:
        '''
        GCSからBigQueryにあげるときにndjson形式だとエラーが発生しにくい為、
        pandas.DataFrameをndjson形式で保存できるようにしている
        '''
        buffer = io.StringIO()
        dataframe.to_json(buffer, orient="records", lines=True, force_ascii=False)
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_string(buffer.getvalue(), content_type=self.mime_type)

    def upload_from_file(self, file_obj) -> None:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_file(file_obj)
