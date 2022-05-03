# How to deploy

---

## 構成定義ファイル ( `app.yaml` )

- Pythonランタイムの指定
  - `runtime: python38`
- エントリポイントの指定
  - デフォルトは、main.py:app
  - `entrypoint: gunicorn -b :$PORT main:app`
- サービス名の指定
  - `service: $YOUR_SERVICE_NAME`
- インスタンスクラスの指定
  - `instance_class: $INSTANCE_CLASS_NAME`
- 環境変数の指定
  - `env_variables: ...`


## gcloud によるデプロイ

```bash
gcloud app deploy ~/my-directory/app.yaml --project=PROJECT_ID
```

> note
> 初回コマンド実行時、`.gcloudignore` が自動生成される

## Service へのアクセス

Entrypoint URL: `https://[service_name]`

---

## References

- [gcloud app deploy | Google Cloud SDK Reference](https://cloud.google.com/sdk/gcloud/reference/app/deploy)
- [App Engine Standard Testing and Deploying | Google Cloud Guide](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app)
- [app yaml 構成定義ファイルリファレンス | Google Cloud Reference](https://cloud.google.com/appengine/docs/standard/python3/config/appref)
