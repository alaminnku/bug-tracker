from fastapi import APIRouter, Cookie
from lib.jwt import auth_user
from models.projects import ProjectCreate, ProjectUpdate
from config.db import db
from bson import ObjectId

router = APIRouter()


# Get all projects
@router.get('/projects')
def get_projects(token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Get and return serialized projects
    projects_response = db.projects.find()

    projects = []
    for project in projects_response:
        project['_id'] = str(project['_id'])
        projects.append(project)
    return projects


# Get a project
@router.get('/projects/{project_id}')
def get_project(project_id: str, token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Get and return the serialized project
    project = db.projects.find_one({'_id': ObjectId(project_id)})
    project['_id'] = str(project['_id'])
    return project


# Create a new project
@router.post('/projects', status_code=201)
def create_project(project: ProjectCreate, token: str = Cookie(None)):
    # Auth user
    user = auth_user(token)

    # Add the creating user id to the members
    project_dict = dict(project)
    project_dict['members'].append(user)

    # Add project to DB
    response = db.projects.insert_one(project_dict)
    inserted_id = response.inserted_id

    # Get and return the created project
    created_project = db.projects.find_one({'_id': ObjectId(inserted_id)})
    created_project['_id'] = str(created_project['_id'])
    return created_project


# Update a project
@router.put('/projects/{project_id}')
def update_project(project_id: str, project: ProjectUpdate, token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Convert JSON member to dictionary
    project_dict = dict(project)
    project_dict['members'] = [dict(member) for member in project_dict['members']]

    # Update the project
    db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': project_dict})

    # Get and return the updated serialized project
    updated_project = db.projects.find_one({'_id': ObjectId(project_id)})
    updated_project['_id'] = str(updated_project['_id'])
    return updated_project
