from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient 


#normally, it is not recommended to share these details with others. So please use your own database.
var_url = f'mongodb+srv://admin:namaskaram@cluster0.vo3dp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'


app = FastAPI()

client = MongoClient(var_url)

dummyDB = client['dummy-database']
dummyCollection = dummyDB['table']
userCollection = dummyDB['userBase']

#Product Model
class Product(BaseModel):
    name: str
    price: int
    eco_friendly: Optional[bool]= None
    is_finalized: Optional[bool] = None

class updateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    eco_friendly: Optional[bool]= None
    is_finalized: Optional[bool] = None

#User Model
class User(BaseModel):
    email: str
    name: str
    work_experience_in_years: int
    position: str
    gender: str
    currently_assigned_to_prject: Optional[bool] = None

class updateUser(BaseModel):
    email:  Optional[str] = None
    name:  Optional[str] = None
    work_experience_in_years: Optional[int] = None
    position:  Optional[str] = None
    gender:  Optional[str] = None
    currently_assigned_to_prject: Optional[bool] = None

# Product CRUD Operations
@app.put("/product/insert")
def insert__product (instance: Product):
    dummyDB.dummyCollection.insert_one(instance.dict())

@app.get("/product/{instance_name}")
def insert__product (instance_name: str):
    for result in dummyDB.dummyCollection.find({"name":instance_name},{"_id":0}):
        if result["name"]==instance_name:
            return result
    return {"Failure":"Product not found"}

@app.get("/product")
def get_all_products():
    x = list()
    results =  dummyDB.dummyCollection.find({},{"_id":0})
    for result in results:
        x.append(result)
    return x

@app.put("/product/update/{instance_name}")
def insert__product (instance_name: str, instance:updateProduct, query:str, updation_value):
    for search in dummyDB.dummyCollection.find({"name":instance_name},{"_id:0"}):
        dummyDB.dummyCollection.update_one(
            {"name": instance_name},
            {"$set":
                {query: updation_value}
            })
        return {"Success":"Updation Successful"}
    return {"Failure":"Product not found"}

@app.delete("/product/delete")
def delete__product (instance_name: str= Path(None, description = "Make sure you enter the right product name!")):
    for search in dummyDB.dummyCollection.find({"name":instance_name},{"_id":0}):
        if search["name"]==instance_name:
            dummyDB.dummyCollection.remove(search)
        return {"Success":"Deletion Successful"}
    return {"Failure":"Product not found"}

    


# User CRUD Operations 
@app.put("/user/insert")
def insert__user (instance: User):
    dummyDB.userCollection.insert_one(instance.dict())

@app.get("/user")
def get_all_users():
    x = list()
    results =  dummyDB.userCollection.find({},{"_id":0})
    for result in results:
        x.append(result)
    return x

@app.get("/user/{user_name}")
def insert__user (user_name: str):
    for result in dummyDB.userCollection.find({"name":user_name},{"_id":0}):
        if result["name"]==user_name:
            return result
    return {"Failure":"User not found"}

@app.put("/user/update/{user_name}")
def insert__product (user_name: str, user:updateUser, query:str, updation_value):
    for search in dummyDB.userCollection.find({"name":user_name},{"_id:0"}):
            dummyDB.userCollection.update_one(
             {"name":user_name},
             {"$set":
                 {query: updation_value}
             })
            return {"Success":"Updation Successful"}
    return {"Failure":"User not found"}

@app.delete("/user/delete")
def delete__product (user_name: str= Path(None, description = "Make sure you enter the right user name!")):
    for search in dummyDB.userCollection.find({"name":user_name},{"_id":0}):
        if search["name"]==user_name:
            dummyDB.userCollection.remove(search)
        return {"Success":"Deletion Successful"}
    return {"Failure":"User not found"}

