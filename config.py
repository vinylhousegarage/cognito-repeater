import os

class Config:
    AWS_COGNITO_AUTHORITY = os.getenv('AWS_COGNITO_AUTHORITY')
    AWS_COGNITO_CLIENT_SECRET = os.getenv('AWS_COGNITO_CLIENT_SECRET')
    AWS_COGNITO_DOMAIN = os.getenv('AWS_COGNITO_DOMAIN')
    AWS_COGNITO_LOGOUT_URI = os.getenv('AWS_COGNITO_LOGOUT_URI')
    AWS_COGNITO_METADATA_URL = os.getenv('AWS_COGNITO_METADATA_URL')
    AWS_COGNITO_REDIRECT_URI = os.getenv('AWS_COGNITO_REDIRECT_URI')
    AWS_COGNITO_SCOPE = os.getenv('AWS_COGNITO_SCOPE', 'openid email profile')
    AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID')
    AWS_COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')

    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')

    FERNET_KEY = os.getenv('FERNET_KEY')

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
