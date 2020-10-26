# User Recommendation API Spec

## Entrypoint

http://localhost:8080

## Resources

### user

|HTTP Method|URL|Explanation|
|:-:|:--|:--|
|GET|/users|ユーザー名一覧を返す|
|GET|/users/search/?kw={topic key word}&max={recommend list max size}|パラメータとして与えたキーワードに関連の高いユーザーを返す。<br>キーワードは、kwパラメータに設定する。<br>maxパラメータに数値を設定すると、レコメンドするユーザー数の最大値を設定できる。|

### channel

|HTTP Method|URL|Explanation|
|:-:|:--|:--|
|GET|/channels|チャンネル名一覧を返す|

## Test

start server (debug mode)

```bash
python main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

http request (curl and jq)

```bash
# GET users
curl -X GET "http://localhost:8080/users" | jq
# GET recommended users
curl -X GET "http://localhost:8080/users/search" -d "kw=test" | jq
curl -X GET "http://localhost:8080/users/search" -d "kw=test" -d "max=5" | jq
```
