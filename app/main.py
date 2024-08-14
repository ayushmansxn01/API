from fastapi import FastAPI
from typing import Optional, List
from . import models
from .database import engine, get_db
from .routers import post,users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or use ["*"] to allow all origins during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# my_posts=[{"title":"title of post 1", "content":"content of post 1", "id":1 },{"title":"my food", "content":"My pizza is comming", "id":2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p


# def find_index(id):
#     for i,p in enumerate(my_posts):
#         if(p['id']==id):
#             return i
        


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}




# EXAMPLE OF USING SQL QUERY
# @app.get("/posts")   #decorator  '/'  => path after the url
# async def get_posts():      #function
#     cursor.execute("""Select * from posts""")  
#     posts=cursor.fetchall()     
#     return posts



