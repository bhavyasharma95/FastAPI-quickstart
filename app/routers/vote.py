from fastapi import Depends, Response, status,HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models,utils,schemas,oauth2
from  ..database import get_db
from app import database

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def oneVote(vote:schemas.Vote,db: Session= Depends(database.get_db),current_user:int =Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"you get one vote")
        newVote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(newVote)
        db.commit()
        return "voted"
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exists")

        vote_query.delete(synchronize_session=False)
        db.commit()   
        return "successfully deleted"  

