from fastapi import FastAPI, Body, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from fastapi.security import HTTPBearer
from jwt_manager import create_token, validate_token

app = FastAPI()
app.title = "smashmentor"
app.version = "1.0.0"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "samsepiol@ecorp.com":
            raise HTTPException(status_code=403, detail="Invalid credentials")

class User(BaseModel):
    email: str
    password: str

class Resource(BaseModel):
    resource_id: int = None
    content: str = Field(min_length = 1, max_length = 1000)
    mode_id: int = Field(ge = 1, le=4)
    resource_type: str = Field(min_length=1)

    model_config={
        "json_schema_extra": {
            "examples": [{
                "resource_id": 1,
                "content": "Type your notes here...",
                "mode_id": 1,
                "resource_type": "Misc."
            }]
        }
    }


modes = [
    {
        'mode_id': 1,
        'name': 'Fundamentals',
        'description': 'Practice your neutral, advantage, disadvantage - and more!'
    },
    {
        'mode_id': 2,
        'name': 'Matchups',
        'description': 'Practice your neutral, advantage, disadvantage - and more!'
    },
    {
        'mode_id': 3,
        'name': 'Tech Skill',
        'description': 'Master various techniques to gain an edge over the competiton!'
    },
    {
        'mode_id': 4,
        'name': 'Mentality',
        'description': 'Learn the art of peak performance'
    }
]

resources = [
    {
        'resource_id': 1,
        'content': 'note 1',
        'mode_id': 1,
        "resource_type": "note"
    },
    {
        'resource_id': 2,
        'content': 'note 2',
        'mode_id': 2,
        "resource_type": "note"
    },
    {
        'resource_id': 3,
        'content': 'note 3',
        'mode_id': 3,
        "resource_type": "note"
    }
]

# LOGIN PAGE
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "samsepiol@ecorp.com" and user.password == "fsox":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)

# MAIN PAGE (INTRODUCTION)
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>THIS IS SMASHMENTOR! (WIP)</h1>')

# GET MODES (RESTRICTED TO LOGIN)
@app.get('/modes', tags=['modes'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_modes():
    return modes

# GET SINGLE MODE (RESTRICTED TO LOGIN)
@app.get('/modes/{id}', tags=['modes'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_mode(id: int):
    return [mode for mode in modes if mode['mode_id'] == id]
    return JSONResponse(content=[], status_code=404)

# GET RESOURCES (RESTRICTED TO LOGIN)
@app.get('/resources', tags=['resources'], response_model=List[Resource], 
status_code=200, dependencies=[Depends(JWTBearer())])
def get_resources() -> List[Resource]:
    return JSONResponse(content=resources)

# GET SINGULAR RESOURCE (RESTRICTED TO LOGIN)
@app.get('/resources/{id}', tags=['resources'], response_model=Resource,
 status_code=200, dependencies=[Depends(JWTBearer())])
def get_resource(id: int) -> Resource:
    for res in resources:
        if res['resource_id'] == id:
            return JSONResponse(content = res)
    return JSONResponse(content = [], status_code = 404)


# GET RESOURCES BY TYPE (RESTRICTED TO LOGIN)
@app.get('/resources/', tags=['resources'], response_model=List[Resource],
 status_code=200, dependencies=[Depends(JWTBearer())])
def get_resources_by_type(type: str) -> List[Resource]:
    res = [item for item in resources if item['resource_type'] == type]
    if len(res) == 0:
        return JSONResponse(content=[], status_code=204)
    return JSONResponse(content=res, status_code=200)

# ADD RESOURCE (RESTRICTED TO LOGIN)
@app.post('/resources', tags=['resources'], response_model=dict,
 status_code=201, dependencies=[Depends(JWTBearer())])
def add_resource(res: Resource) -> dict:
    resources.append({
        'resource_id': res.resource_id,
        'content': res.content,
        'mode_id': res.mode_id,
        'resource_type': res.resource_type
    })
    return JSONResponse(content={'message': 'Succesfully added resource'})

# MODIFY RESOURCE
@app.put('/resources', tags=['resources'], response_model=dict,
 status_code=200, dependencies=[Depends(JWTBearer())])
def modify_resource(id: int, res: Resource) -> dict:
    for item in resources:
        if item['resource_id'] == id:
            item['content'] = res.content
            item['mode_id'] = res.mode_id
            item['resource_type'] = res.resource_type
            return JSONResponse(content={'message': 'Succesfully modified resource'})
    return JSONResponse(content={'message': 'Resource not found, nothing modified'}, status_code=400)

# DELETE RESOURCE (RESTRICTED TO LOGIN)
@app.delete('/resources', tags=['resources'], response_model=dict,
 status_code=200, dependencies=[Depends(JWTBearer())])
def delete_resource(id: int) -> dict:
    for item in resources:
        if item['resource_id'] == id:
            resources.remove(item)
            return JSONResponse(content={'message': 'Resource succesfully deleted'})
    return JSONResponse(content={'Resource not found, nothing deleted'}, status_code=400)
