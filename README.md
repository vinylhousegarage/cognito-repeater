## Cognito Repeater ( Cognito 認証中継 API )

### 1. 概要
  - **目的**
    - 本 API は、AWS Cognito が発行する access_token の署名および標準クレームの検証を目的としています。

  - **提供機能**
    - Cognito へのログインおよびログアウト
    - access_token の署名および標準クレーム（iss・aud・exp）の検証
    - ユーザーアカウントの有効確認

### 2. ルートURL
  - ### [https://cognito-repeater.com](https://cognito-repeater.com)
  - ルートURL へのアクセスは /login にリダイレクトされます。

### 3. エンドポイント
  - **すべてのエンドポイントは、ルートURL に対する相対パスです。**

| メソッド | パス      | 用途                     |戻り値              |
|-----|---------------|--------------------------|--------------------------|
| GET | /metadata |本 API のエンドポイント一覧の取得|エンドポイント一覧|
| GET | /login |Cognito のログイン画面にリダイレクト|リダイレクト|
| GET | /token |署名および標準クレーム (iss・aud・exp) の検証|sub (access_token が正当の場合)|
| GET | /user |Cognito のユーザーアカウントの有効確認|sub (ユーザーアカウントが有効の場合)|
| GET | /logout |Cognito からのログアウト処理およびリダイレクト|リダイレクト|
| GET | /docs |本 API の GUI ドキュメントを取得|Swagger UI ドキュメント|
| GET | /redoc |本 API の ReDoc 形式ドキュメントを取得|ReDoc 形式ドキュメント|
| GET | /openapi.json |本 API の OpenAPI 仕様の JSON ファイルを取得|OpenAPI 仕様の JSON ファイル|

  - **以下のエンドポイントでは、Authorization ヘッダーに Bearer <access_token> を指定する必要があります。**

| メソッド | パス |
|-----|----------|
| GET | /token |
| GET | /user |
| GET | /docs |
| GET | /redoc |
| GET | /openapi.json |

  - **以下のエンドポイントでは、使用方法や仕様を確認できる自動生成ドキュメントを提供しています。**

| メソッド | パス |
|-----|----------|
| GET | /docs |
| GET | /redoc |
| GET | /openapi.json |

### 4. システム構成
  - **技術スタック**
    - プログラミング言語：Python 3.11.11
    - フレームワーク：FastAPI 0.115.12
    - 認証機能：AWS Cognito
    - 仮想環境構築：Docker
      - 開発環境：Docker で Dockerコンテナを起動
      - 本番環境：AWS Lambda で Dockerイメージを使用
    - テスト環境：GitHub Actions
    - ローカル環境のバージョン管理：Git
    - リモートリポジトリのホスティング：GitHub
    - CI/CD：GitHub Actions

  - **インフラ構成**
    - API 実行クラウド：AWS
    - API 実行環境：Lambda
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
  - この API は [MIT License](https://opensource.org/licenses/MIT) のもとで公開されています。
