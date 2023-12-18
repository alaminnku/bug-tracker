from fastapi import APIRouter
from models.projects import BugCreate, BugUpdate
from config.db import db
from bson import ObjectId

router = APIRouter()


# Get a projects bugs
@router.get('/projects/{project_id}/bugs')
async def get_bugs(project_id):
    return {'message': 'Get bugs'}


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

    # Update add the bug to the project
    bug_response = db.projects.find_one_and_update(
        {'_id': ObjectId(project_id)}, {'$push': {'bugs': bug_dict}}
    )
    bug_response['id'] = str(bug_response.pop('_id'))
    return bug_response


# Update a bug
@router.put('/projects/{project_id}/bugs/{bug_id}')
async def get_bugs(project_id, bug_id):
    return {'message': 'Update bug'}
