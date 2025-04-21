import os

class Config:
    def __init__(self):
        self.AWS_COGNITO_AUTHORITY = os.getenv('AWS_COGNITO_AUTHORITY')
        self.AWS_COGNITO_CLIENT_SECRET = os.getenv('AWS_COGNITO_CLIENT_SECRET')
        self.AWS_COGNITO_DOMAIN = os.getenv('AWS_COGNITO_DOMAIN')
        self.AWS_COGNITO_LOGOUT_URI = os.getenv('AWS_COGNITO_LOGOUT_URI')
        self.AWS_COGNITO_METADATA_URL = os.getenv('AWS_COGNITO_METADATA_URL')
        self.AWS_COGNITO_REDIRECT_URI = os.getenv('AWS_COGNITO_REDIRECT_URI')
        self.AWS_COGNITO_SCOPE = os.getenv('AWS_COGNITO_SCOPE', 'openid email profile')
        self.AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID')
        self.AWS_COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')

        self.AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')

        self.FERNET_KEY = os.getenv('FERNET_KEY')

        self.SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
