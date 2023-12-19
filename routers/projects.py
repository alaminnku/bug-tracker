from fastapi import APIRouter, Cookie
from lib.auth import auth_user
from models.projects import ProjectCreate, ProjectUpdate
from config.db import db
from bson import ObjectId
from lib.utils import serialize_project

router = APIRouter()


# Get all projects
@router.get('/projects')
def get_projects(token: str = Cookie(None)):
    # Authenticate user
    auth_user(token)

    # Get and return serialized projects
    projects_response = db.projects.find()

    # Return the serialized projects
    projects = [serialize_project(project) for project in projects_response]
    return projects


# Get a project
@router.get('/projects/{project_id}')
def get_project(
    project_id: str,
    token: str = Cookie(None)
):
    # Authenticate user
    auth_user(token)

    # Get the project
    project_response = db.projects.find_one({'_id': ObjectId(project_id)})

    # Return the serialized project
    project = serialize_project(project_response)
    return project


# Create a new project
@router.post('/projects', status_code=201)
def create_project(
    project: ProjectCreate,
    token: str = Cookie(None)
):
    # Auth user
    user = auth_user(token)

    # Add the creating user id to the members
    project_dict = dict(project)
    project_dict['members'].append(user)

    # Add project to DB
    response = db.projects.insert_one(project_dict)
    inserted_id = response.inserted_id

    # Get the created project
    created_response = db.projects.find_one({'_id': ObjectId(inserted_id)})

    # Return the serialized project
    created_project = serialize_project(created_response)
    return created_project


# Update a project
@router.put('/projects/{project_id}')
def update_project(
    project_id: str,
    project: ProjectUpdate,
    token: str = Cookie(None)
):
    # Authenticate user
    auth_user(token)

    # Convert JSON member to dictionary
    project_dict = dict(project)
    project_dict['members'] = [
        dict(member) for member in project_dict['members']
    ]

    # Update the project
    updated_response = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id)
        },
        {
            '$set': project_dict
        },
        return_document=True
    )

    # Return the serialized project
    updated_project = serialize_project(updated_response)
    return updated_project
