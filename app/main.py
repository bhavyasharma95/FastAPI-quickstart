from fastapi import FastAPI
from . import models
from .database import engine
import requests
import random
from fastapi.middleware.cors import CORSMiddleware


from .routers import posts,users, auth, vote


models.Base.metadata.create_all(bind=engine) ##This line creates the models on postgres

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)   

@app.get("/")
async def root():
    number = random.randint(101, 999)
    xkcd = requests.get(f"https://xkcd.com/{number}/info.0.json").json()
    return xkcd
 

    

