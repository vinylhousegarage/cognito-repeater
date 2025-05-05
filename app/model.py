from pydantic import BaseModel, validator

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

    @validator('*')
    def must_start_with_slash(cls, v, field):
        if not v.startswith('/'):
            raise ValueError(f"{field.name} must start with '/'")
        return v
