from pydantic import BaseModel, Field, validator

class MetadataResponse(BaseModel):
    login_endpoint: str = Field(..., description="Must start with '/'")
    logout_endpoint: str = Field(..., description="Must start with '/'")
    verify_access_token_endpoint: str = Field(..., description="Must start with '/'")
    verify_userinfo_endpoint: str = Field(..., description="Must start with '/'")
    health_check_endpoint: str = Field(..., description="Must start with '/'")
    simulate_404_endpoint: str = Field(..., description="Must start with '/'")
    docs_url: str = Field(..., description="Must start with '/'")
    redoc_url: str = Field(..., description="Must start with '/'")
    openapi_url: str = Field(..., description="Must start with '/'")

    @validator('*')
    def must_start_with_slash(cls, v, field):
        if not v.startswith('/'):
            raise ValueError(f"{field.name} must start with '/'")
        return v
