from ast import Delete
from asyncio.windows_events import NULL
from logging import raiseExceptions
import stat
from turtle import title
from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content : str
    published : bool=True
    rating : Optional[int]=None


my_posts = [
            {"title" :"title of post 1","content":"content of post 1","id":1},
            {"title" :"Favorite Food","content": "Pizza","id":2}
            ]




def find_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p
        else :
            pass

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return int(i)

#first page 
@app.get("/")
def root():
    return {"message": "it's getting fun over here"}


#getting all posts
@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


#getting just one post
@app.get("/posts/{id}")
def get_one_post(id : int, response : Response):
    post = find_post(id)
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    return {"data" : post}


## creating one post and add it to database
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createposts(new_post : Post ):
    my_post_dict = new_post.dict()
    my_post_dict['id'] = randrange(0,1000000) 
    my_posts.append(my_post_dict)
    return{"data" : my_post_dict}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    index_post = find_index_post(id)

    if index_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} doesn't exist")
    my_posts.pop(index_post)
    return {Response(status_code=status.HTTP_204_NO_CONTENT)}


def test():
    print("hello world")
    pass


    


