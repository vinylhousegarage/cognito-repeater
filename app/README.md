# API 概要

本アプリは、AWS Cognito が発行する access_token の署名および標準クレームを検証する API と、各種ユーティリティエンドポイントを提供します。

## ルートURL
 https://cognito-repeater.com

※ 以下のすべてのエンドポイントは、ルートURL に対する相対パスです。

## エンドポイント詳細

- GET /metadata：本アプリで提供されている APIエンドポイント の一覧を返します。
- GET /login：Cognito のログイン画面にリダイレクトします。
- GET /me：access_token の署名および標準クレーム（iss, aud, exp）を検証し、正当であれば sub を返します。
- GET /sub：Cognito の userinfo エンドポイントを呼び出し、ユーザーアカウントが有効であれば sub を返します。
- GET /logout：Cognito からログアウトし、ログアウトページにリダイレクトします。

### Authorization ヘッダーが必要なエンドポイント

以下のエンドポイントでは、Authorization ヘッダーに Bearer <access_token> を指定する必要があります。

- /me
- /sub

## API ドキュメント（Swagger UI）

本アプリは、自動生成された APIドキュメント を提供しています。

- /docs：Swagger UI 仕様の GUI ドキュメント
- /redoc：ReDoc 形式 のドキュメント
- /openapi.json：OpenAPI 仕様の JSON ファイル

## ライセンス

このアプリケーションは [MIT License](https://opensource.org/licenses/MIT) のもとで公開されています。
