from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/error/404')
def trigger_404():
    raise HTTPException(status_code=404, detail='This is a test 404')
