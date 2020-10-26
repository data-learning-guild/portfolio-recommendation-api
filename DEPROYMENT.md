# How to deploy

## ref

- [gcloud app deploy | Google Cloud SDK Reference](https://cloud.google.com/sdk/gcloud/reference/app/deploy)
- [App Engine Standard Testing and Deploying | Google Cloud Guide](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app)
- [app yaml 構成定義ファイルリファレンス | Google Cloud Reference](https://cloud.google.com/appengine/docs/standard/python3/config/appref)

## 構成定義ファイル

- エントリポイントの指定
  - デフォルトは、main.py:app
  - `entrypoint: gunicorn -b :$PORT main:app`
- Pythonランタイムの指定


## gcloud によるデプロイ

```bash
gcloud app deploy ~/my-directory/app.yaml --project=PROJECT_ID
```

> note
> 初回コマンド実行時、`.gcloudignore` が自動生成される

## Service へのアクセス

Entrypoint URL: `https://[service_name]`
