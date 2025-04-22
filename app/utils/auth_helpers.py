from fastapi.responses import RedirectResponse

def redirect_to_cognito_login() -> RedirectResponse:
    return RedirectResponse(url='https://example.com/login')
