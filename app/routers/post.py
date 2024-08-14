

from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import  List
from typing import Optional

from sqlalchemy import func



router=APIRouter(
     prefix="/posts",
     tags=['Posts']
)

# @router.get("/", response_model=List[schemas.PostOut])   #decorator  '/'  => path after the url
@router.get("/") 

def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0, search:Optional[str]=" " ):      #function
    # cursor.execute("""Select * from posts""")  
    # posts=cursor.fetchall()  



    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()   
    print("gcytdgf")

    results=db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(type(results))

    formatted_results = []
    for post, votes in results:
        post_data = post.__dict__.copy()  # Convert SQLAlchemy object to dict
        post_data['votes'] = votes        # Add the votes count to the dict
        post_data.pop('_sa_instance_state', None)  # Remove internal SQLAlchemy attribute
        formatted_results.append(post_data)

    

    return formatted_results


# @app.post("/createposts")
# async def create_posts(payload :dict=Body(...)):     #extract all fields from body and save to python dictionary named payload
#     print(payload)
#     return {"new_post":f"title {payload['title']} content:{payload['title']} "}




@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post:schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):     #extract all fields from body and save to python dictionary named payload


    # cursor.execute(""" insert into posts(title,content,published) values(%s,%s,%s) returning *""", (new_post.title, new_post.content,new_post.published))     #to prevent sql injection
    
    # res_post=cursor.fetchone()
    # conn.commit()


    # res_post=models.Post(title=new_post.title, content=new_post.content,published=new_post.published )
    print(current_user.email)
    res_post=models.Post(owner_id=current_user.id,**new_post.dict())
    db.add(res_post)
    db.commit()
    db.refresh(res_post) # to retrieve the new post created and save it in new_post 
    return res_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
            ):         #to accept input in integer only

    #2
    # cursor.execute(""" select * from posts where id=%s""", (str(id)))
    # test_post=cursor.fetchone()
    # print(test_post)

    test_post=db.query(models.Post).filter(models.Post.id==id).first() # to give the first result only sincee id is unique
    print(test_post)

    if not test_post:

        #1
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id:{id} not found"}



        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    return  test_post




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT )
def delete_post(id:int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # cursor.execute(""" delete from posts where id=%s returning * """, (str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()


    post_query_to_delete=db.query(models.Post).filter(models.Post.id==id)

    post=post_query_to_delete.first()

    if post_query_to_delete.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request")

    post_query_to_delete.delete(synchronize_session=False)
    db.commit()

    return  Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,  db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" update posts set title=%s, content=%s where id=%s returning *""" , (post.title,post.content,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)     #saving query
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

