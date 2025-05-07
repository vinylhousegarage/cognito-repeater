## Cognito Repeater ( Cognito 認証中継アプリ )

### 1. 概要
  - **目的**
    - 本アプリは、AWS Cognito が発行する access_token の署名および標準クレームの検証を目的としています。

  - **提供機能**
    - Cognito へのログインおよびログアウト
    - access_token の署名および標準クレーム（iss・aud・exp）の検証
    - ユーザーアカウントの有効確認

### 2. ルートURL
  - ### [https://cognito-repeater.com](https://cognito-repeater.com)
  - ルートURL へのアクセスは /login にリダイレクトされます。

### 3. エンドポイント
  - **すべてのエンドポイントは、ルートURL に対する相対パスです。**

    - GET /metadata：本 API で提供されているエンドポイントの一覧を返します。
    - GET /login：Cognito のログイン画面にリダイレクトします。
    - GET /token：access_token の署名および標準クレーム（iss, aud, exp）を検証し、正当であれば sub を返します。
    - GET /user：Cognito の userinfo エンドポイントを呼び出し、ユーザーアカウントが有効であれば sub を返します。
    - GET /logout：Cognito からログアウトし、ログアウトページにリダイレクトします。
    - GET /docs：Swagger UI 仕様の GUI ドキュメントを返します。
    - GET /redoc：ReDoc 形式 のドキュメントを返します。
    - GET /openapi.json：OpenAPI 仕様の JSON ファイルを返します。

  - **以下のエンドポイントでは、Authorization ヘッダーに Bearer <access_token> を指定する必要があります。**

    - GET /token
    - GET /user
    - GET /docs
    - GET /redoc
    - GET /openapi.json

  - **以下のエンドポイントでは、使用方法や仕様を確認できる自動生成ドキュメントを提供しています。**

    - GET /docs
    - GET /redoc
    - GET /openapi.json

### 4. システム構成
  - **技術スタック**
    - プログラミング言語：Python 3.11.11
    - フレームワーク：FastAPI 0.115.12
    - 認証機能：AWS Cognito
    - 仮想環境構築：Docker
      - 開発環境：Docker で Dockerコンテナを起動
      - 本番環境：AWS Lambda で Dockerイメージを使用
    - テスト環境：GitHub Actions
    - ソースコードのローカルバージョン管理：Git
    - リモートリポジトリのホスティング：GitHub
    - CI/CD：GitHub Actions

  - **インフラ構成**
    - 開発環境サーバー：Uvicorn
    - アプリのホスティング：AWS
      - アプリ実行：Lambda
      - イメージ管理：ECR
      - ハンドラー：Mangum
      - API Gateway：HTTP API
      - 構成管理：SSM ( パラメータストア )
      - ドメイン・DNS管理：Route 53

### 5. アクセス情報
  - **GitHubリポジトリURL**
    - [https://github.com/vinylhousegarage/cognito-repeater](https://github.com/vinylhousegarage/cognito-repeater)
  - **アプリURL**
    - [https://cognito-repeater.com](https://cognito-repeater.com)

### 6. ライセンス
  - このアプリは [MIT License](https://opensource.org/licenses/MIT) のもとで公開されています。
