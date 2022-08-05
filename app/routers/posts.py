from fastapi import Depends, Response, status,HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models,utils,schemas,oauth2
from  ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[schemas.PostOut])
def getPost(db: Session = Depends(get_db),search:Optional[str]= ""):
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).all()
    # post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).all()
    return post

@router.get("/{id}",response_model=schemas.Post)
def getOnePost(id:int, db: Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    newPost = models.Post(owner_id=current_user.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.put("/{id}",response_model=schemas.Post)
def updatePost(id:int,updatedPost:schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist" )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"update your post" )       
    postQuery.update(updatedPost.dict(),synchronize_session=False)
    db.commit()

    return postQuery.first()    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post= postQuery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist" )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"delete your post" )       
    postQuery.delete(synchronize_session=False)  
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 