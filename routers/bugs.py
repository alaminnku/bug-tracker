from fastapi import APIRouter
from models.projects import BugCreate, BugUpdate
from config.db import db
from bson import ObjectId

router = APIRouter()


# Get a projects bugs
@router.get('/projects/{project_id}/bugs')
async def get_bugs(project_id: str):
    project = db.projects.find_one({'_id': ObjectId(project_id)})
    return project['bugs']


# Get a specific bug
@router.get('/projects/{project_id}/bugs/{bug_id}')
async def get_bugs(project_id, bug_id):
    return {'message': 'Get a bug'}


# Create a new bug
@router.post('/projects/{project_id}/bugs')
async def create_bug(bug: BugCreate, project_id: str):
    # Convert bug data to dict
    bug_dict = dict(bug)
    bug_dict['reported_by'] = dict(bug_dict['reported_by'])
    bug_dict['assigned_to'] = dict(bug_dict['assigned_to'])


    # Add the bug to the project
    db.projects.find_one_and_update(
        {'_id': ObjectId(project_id)}, {'$push': {'bugs': bug_dict}}
    )

    # Return the updated project
    updated_project = db.projects.find_one({'_id': ObjectId(project_id)})
    updated_project['id'] = str(updated_project.pop('_id'))
    return updated_project


# Update a bug
@router.put('/projects/{project_id}/bugs/{bug_id}')
async def get_bugs(project_id, bug_id):
    return {'message': 'Update bug'}
