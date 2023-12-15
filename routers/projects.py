from fastapi import APIRouter, Request, Cookie
from lib.jwt import auth_user
from models.projects import Project
from config.db import db
from schema.projects import serialize_project, serialize_projects
from bson import ObjectId

router = APIRouter()


# Get all projects
@router.get('/projects')
async def get_projects(token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Get and return serialized projects
    response = db.projects.find()
    serialized_project = serialize_projects(response)
    return serialized_project


# Get a project
@router.get('/projects/{project_id}')
async def get_project(request: Request, project_id):
    return {'message': f'Get a project {project_id}'}


# Create a new project
@router.post('/projects')
async def create_project(project: Project, token: str = Cookie(None)):
    # Auth user 
    user = auth_user(token)

    # Add the creating user id to the members
    project_dict = dict(project)
    project_dict['members'].append(user['id'])

    # Add project to DB
    response = db.projects.insert_one(project_dict)
    inserted_id = response.inserted_id

    # Get the added project
    project_response = db.projects.find_one({'_id': ObjectId(inserted_id)})
    
    # Return the serialized project
    serialized_project = serialize_project(project_response) 
    return serialized_project


# Update a project
@router.put('/projects/{project_id}')
async def update_project(request: Request, project_id):
    return {'message': 'Update project'}

