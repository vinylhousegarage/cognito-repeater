## Cognito Repeater ( AWS Cognito 認証・中継 API )

### 1. 概要
  - **目的**
    - 本 API は、複数アプリ間で共通利用できるログイン機能を提供することを目的としています。

  - **提供機能**
    - AWS Cognito へのログインおよびログアウト
    - AWS Cognito が発行する access_token の署名および標準クレーム（iss・aud・exp）の検証
    - AWS Cognito で認証されたユーザーアカウントの有効確認

### 2. ルートURL
  - ### [https://cognito-repeater.com](https://cognito-repeater.com)
  -  ルートURL にアクセスすると自動的に /login に転送され、Cognito ログイン画面が表示されます。

### 3. エンドポイント
  - すべてのエンドポイントは、ルートURL に対する相対パスです。
  - 認証指定欄が『必要』のエンドポイントは、Authorization ヘッダーに Bearer <access_token> を指定する必要があります。

| メソッド | パス      | 用途                     |認証指定|戻り値              |
|-----|---------------|--------------------------|----|----------------------|
| GET | /metadata |本 API のエンドポイント一覧の取得||各エンドポイントのパスを格納した JSON オブジェクト|
| GET | /health |本 API の稼働確認||{"status": "ok"}|
| GET | /error/404 |本 API の 404 エラーの動作確認||HTTP 404 ({"detail": "This is a test 404"})|
| GET | /login |Cognito へのログイン処理||Cognito のログイン画面へリダイレクト|
| GET | /token |署名および標準クレーム (iss・aud・exp) の検証|必要|{"sub": "<UUID形式のユーザーID>"}|
| GET | /user |Cognito のユーザーアカウントの有効確認|必要|{"sub": "<UUID形式のユーザーID>"}|
| GET | /logout |Cognito からのログアウト処理||{"message": "Logout successful"}|
| GET | /docs |本 API の GUI ドキュメントの取得|必要|Swagger UI ドキュメント|
| GET | /redoc |本 API の ReDoc 形式ドキュメントの取得|必要|ReDoc 形式ドキュメント|
| GET | /openapi.json |本 API の OpenAPI 仕様の取得|必要|OpenAPI 仕様の JSON ファイル|

### 4. システム構成
  - **技術スタック**
    | カテゴリー | 選定技術 |
    | --- | --- |
    | 開発言語 | Python 3.11.11 |
    | フレームワーク | FastAPI 0.115.12 |
    | ソース管理 | Git |
    | リポジトリ | GitHub |
    | CI/CD | GitHub Actions |
    | 開発環境 | Docker |

  - **インフラ構成（AWS）**
    | コンポーネント | 採用サービス・ツール |
    | :--- | :--- |
    | ドメイン登録 | Route 53 |
    | DNS管理 | Route 53 |
    | 証明書管理 | ACM |
    | API接点 | API Gateway |
    | APIタイプ | HTTP API |
    | 認証基盤 | Cognito |
    | 実行基盤 | Lambda |
    | 変換アダプター | Mangum |
    | 秘匿情報管理 | SSM Parameter Store（SecureString） |
    | イメージ管理 | ECR |

### 5. ライセンス
  - 本 API は [MIT License](https://opensource.org/licenses/MIT) のもとで公開されています。
