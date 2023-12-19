from fastapi import APIRouter, Cookie
from models.projects import BugCreate, BugUpdate
from config.db import db
from bson import ObjectId
from lib.auth import auth_user

router = APIRouter()


# Get a projects bugs
@router.get('/projects/{project_id}/bugs')
async def get_bugs(
    project_id: str,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Get the project
    project = db.projects.find_one({'_id': ObjectId(project_id)})

    # Format and return the bugs
    bugs = [
        {
            'id': str(bug.pop('_id')),
            **bug
        } for bug in project.get('bugs', [])]

    return bugs


# Get a specific bug
@router.get('/projects/{project_id}/bugs/{bug_id}')
async def get_bug(
    project_id: str,
    bug_id: str,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Get the project
    project = db.projects.find_one({'_id': ObjectId(project_id)})

    # Get, update and return the bug
    found_bug = next(
        (bug for bug in project['bugs'] if str(bug['_id']) == bug_id), None)
    found_bug['id'] = str(found_bug.pop('_id'))
    return found_bug


# Create a new bug
@router.post('/projects/{project_id}/bugs')
async def create_bug(
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
    updated_project = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id)
        },
        {
            '$push': {'bugs': bug_dict}
        },
        return_document=True
    )

    # Update the project and bug ids
    updated_project['id'] = str(updated_project.pop('_id'))
    updated_project['bugs'] = [
        {
            'id': str(bug.pop('_id')),
            **bug
        } for bug in updated_project['bugs']]

    # Return the updated project
    return updated_project


# Update a bug
@router.put('/projects/{project_id}/bugs/{bug_id}')
async def update_bug(
    project_id: str,
    bug_id: str, bug:
    BugUpdate,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Convert bug data to dict
    bug_dict = dict(bug)
    bug_dict['reported_by'] = dict(bug_dict['reported_by'])
    bug_dict['assigned_to'] = dict(bug_dict['assigned_to'])

    # Update the bug
    updated_project = db.projects.find_one_and_update(
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
                'bugs.$.comments': bug_dict['comments'],
            }
        },
        return_document=True)

    # Convert ObjectId to id
    updated_project['id'] = str(updated_project.pop('_id'))
    updated_project['bugs'] = [
        {
            'id': str(updated_bug.pop('_id')),
            **updated_bug
        } for updated_bug in updated_project.get('bugs', [])]

    # Return the updated projected
    return updated_project
