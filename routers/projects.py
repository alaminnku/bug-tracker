from fastapi import APIRouter, Request, HTTPException, Cookie
from lib.jwt import auth_user

router = APIRouter()


# Get all projects
@router.get('/projects')
async def get_projects(request: Request, token: str = Cookie(None)):
    user = auth_user(token)
    print(user)
    return {'message': 'Get tasks'}


# Get a project
@router.get('/projects/{project_id}')
async def get_project(request: Request, project_id):
    return {'message': f'Get a project {project_id}'}


# Create a new project
@router.post('/projects')
async def create_projects(request: Request): 
    print(request.state.user)
    return {'message': 'Create task'}


# Update a project
@router.put('/projects/{project_id}')
async def update_project(request: Request, project_id):
    return {'message': 'Update project'}

