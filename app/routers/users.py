from fastapi import FastAPI, Depends, Response, status,HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models,utils,schemas
from  ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def createUser(user:schemas.UserCreate,db: Session = Depends(get_db)):
    # hashing the password and then updating it in user schema 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{id}",response_model=schemas.UserOut)
def getUser(id:int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user    
