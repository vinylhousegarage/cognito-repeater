from pydantic import BaseModel, field_validator

class MetadataResponse(BaseModel):
    login_endpoint: str
    logout_endpoint: str
    verify_access_token_endpoint: str
    verify_userinfo_endpoint: str
    health_check_endpoint: str
    simulate_404_endpoint: str
    docs_url: str
    redoc_url: str
    openapi_url: str

    @field_validator('*', mode='before')
    @classmethod
    def must_start_with_slash(cls, v, info):
        if not isinstance(v, str):
            raise TypeError(f'{info.field_name} must be a string')
        if not v.startswith('/'):
            raise ValueError(f"{info.field_name} must start with '/'")
        return v
