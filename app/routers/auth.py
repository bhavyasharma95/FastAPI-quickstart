from fastapi import FastAPI, Depends, Response, status,HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models,utils,schemas,database, oauth2


router = APIRouter(
    prefix="/login",
    tags=["auth"]
)

@router.post("/",response_model=schemas.Token)
def getLogin(user_Credentials:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_Credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"wrong credentials")

    if not utils.verify(user_Credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"wrong credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}    

