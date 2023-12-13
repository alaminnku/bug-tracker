from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


# Get all projects
@router.get('/projects')
async def get_projects(request: Request):
    print(request.state.user)
    return {'message': 'Get tasks'}


@router.get('/projects/{project_id}')
async def get_project(request: Request):
    return {'message': 'Get a project'}


# Create a new project
@router.post('/projects')
async def create_projects(request: Request): 
    print(request.state.user)
    return {'message': 'Create task'}


# Update a project
@router.put('/projects/{project_id}')
async def update_project(request: Request):
    return {'message': 'Update project'}

