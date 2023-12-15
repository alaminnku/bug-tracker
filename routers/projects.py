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
async def get_project(project_id: str, token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Get and return the serialized project
    response = db.projects.find_one({'_id': ObjectId(project_id)})
    serialized_project = serialize_project(response)
    return serialized_project


# Create a new project
@router.post('/projects', status_code=201)
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
async def update_project(project_id: str, project: Project, token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Update the project
    db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': dict(project)})

    # Get and return the updated serialized project
    response = db.projects.find_one({'_id': ObjectId(project_id)})
    serialized_project = serialize_project(response)
    return serialized_project

