from pydantic import BaseModel

class CreateUser(BaseModel):

 username:str

 name:str
 surname:str
 address:str

 password:str

