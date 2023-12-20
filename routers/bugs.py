from fastapi import APIRouter, Cookie
from models.bugs import BugCreate, BugUpdate
from config.db import db
from bson import ObjectId
from lib.auth import auth_user
from lib.utils import serialize_project, serialize_bug

router = APIRouter()


# Get a projects bugs
@router.get('/projects/{project_id}/bugs')
def get_bugs(
    project_id: str,
    token=Cookie(None)
):
    # Authenticate user
    auth_user(token)

    # Get the project
    project = db.projects.find_one(
        {
            '_id': ObjectId(project_id)
        },
        {
            'created_at': 0,
            'updated_at': 0
        }
    )

    # Format and return the bugs
    bugs = [serialize_bug(bug) for bug in project.get('bugs', [])]
    return bugs


# Get a specific bug
@router.get('/projects/{project_id}/bugs/{bug_id}')
def get_bug(
    project_id: str,
    bug_id: str,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Get the project
    project = db.projects.find_one(
        {
            '_id': ObjectId(project_id)
        },
        {
            'created_at': 0,
            'updated_at': 0
        }
    )

    # Find, serialize and return the bug
    found_bug = next(
        (bug for bug in project['bugs'] if str(bug['_id']) == bug_id), None
    )
    bug = serialize_bug(found_bug)
    return bug


# Create a new bug
@router.post('/projects/{project_id}/bugs')
def create_bug(
    bug: BugCreate,
    project_id: str,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Convert bug data to dict
    bug_dict = dict(bug)
    bug_dict['_id'] = ObjectId()
    bug_dict['reported_by'] = dict(bug_dict['reported_by'])
    bug_dict['assigned_to'] = dict(bug_dict['assigned_to'])

    # Add the bug to the project
    project_response = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id)
        },
        {
            '$push': {'bugs': bug_dict}
        },
        {
            'created_at': 0,
            'updated_at': 0
        },
        return_document=True
    )

    # Serialize and return the project
    updated_project = serialize_project(project_response)
    return updated_project


# Update a bug
@router.put('/projects/{project_id}/bugs/{bug_id}')
def update_bug(
    project_id: str,
    bug_id: str,
    bug: BugUpdate,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Convert bug data to dict
    bug_dict = dict(bug)
    bug_dict['reported_by'] = dict(bug_dict['reported_by'])
    bug_dict['assigned_to'] = dict(bug_dict['assigned_to'])

    # Update the bug
    project_response = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id),
            'bugs._id': ObjectId(bug_id)
        },
        {
            '$set': {
                'bugs.$.title': bug_dict['title'],
                'bugs.$.description': bug_dict['description'],
                'bugs.$.status': bug_dict['status'],
                'bugs.$.severity': bug_dict['severity'],
                'bugs.$.priority': bug_dict['priority'],
                'bugs.$.reported_by': bug_dict['reported_by'],
                'bugs.$.assigned_to': bug_dict['assigned_to'],
                'bugs.$.updated_at': bug_dict['updated_at']
            }
        },
        {
            'created_at': 0,
            'updated_at': 0
        },
        return_document=True)

    # Serialize and return the project
    updated_project = serialize_project(project_response)
    return updated_project
