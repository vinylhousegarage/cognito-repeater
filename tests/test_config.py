import os
import pytest

from app.config import Config

def test_config_returns_environment_variables(monkeypatch):
    monkeypatch.setenv('AWS_ACCOUNT_ID', 'account-id')
    monkeypatch.setenv('AWS_COGNITO_AUTHORITY', 'https://authority')
    monkeypatch.setenv('AWS_COGNITO_CLIENT_SECRET', 'client-secret')
    monkeypatch.setenv('AWS_COGNITO_DOMAIN', 'https://domain')
    monkeypatch.setenv('AWS_COGNITO_LOGOUT_URI', 'http://logout-uri')
    monkeypatch.setenv('AWS_COGNITO_METADATA_URL', 'https://metadata-url')
    monkeypatch.setenv('AWS_COGNITO_REDIRECT_URI', 'https://redirect-uri')
    monkeypatch.setenv('AWS_COGNITO_SCOPE', 'scope')
    monkeypatch.setenv('AWS_COGNITO_USER_POOL_CLIENT_ID', 'user-pool-client-id')
    monkeypatch.setenv('AWS_COGNITO_USER_POOL_ID', 'user-pool-id')
    monkeypatch.setenv('AWS_REGION', 'region')
    monkeypatch.setenv('FERNET_KEY', 'fernet-key')
    monkeypatch.setenv('SECRET_KEY', 'secret-key')

    config = Config()

    assert config.AWS_COGNITO_AUTHORITY == 'https://authority'
    assert config.AWS_COGNITO_CLIENT_SECRET == 'client-secret'
    assert config.AWS_COGNITO_DOMAIN == 'https://domain'
    assert config.AWS_COGNITO_LOGOUT_URI == 'http://logout-uri'
    assert config.AWS_COGNITO_METADATA_URL == 'https://metadata-url'
    assert config.AWS_COGNITO_REDIRECT_URI == 'https://redirect-uri'
    assert config.AWS_COGNITO_SCOPE == 'scope'
    assert config.AWS_COGNITO_USER_POOL_CLIENT_ID == 'user-pool-client-id'
    assert config.AWS_COGNITO_USER_POOL_ID == 'user-pool-id'
    assert config.AWS_REGION == 'region'
    assert config.FERNET_KEY == 'fernet-key'
    assert config.SECRET_KEY == 'secret-key'
