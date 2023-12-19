from fastapi import APIRouter, Cookie
from config.db import db
from bson import ObjectId
from models.comments import CommentCreate, CommentUpdate
from lib.auth import auth_user
from lib.utils import serialize_project


router = APIRouter()


# Get all comments
@router.get('/projects/{project_id}/bugs/{bug_id}/comments')
async def get_comments(
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

    # Get the bug
    bug = next((bug for bug in project['bugs']
               if str(bug['_id'] == bug_id)), None)

    # Convert comment ObjectId to id
    comments = [
        {
            'id': str(comment.pop('_id')),
            **comment
        } for comment in bug.get('comments', [])]

    # Return comments
    return comments


# Create a new comment
@router.post('/projects/{project_id}/bugs/{bug_id}/comments')
async def create_comment(
    project_id: str,
    bug_id: str,
    comment: CommentCreate,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    # Convert model to dict
    comment_dict = dict(comment)
    comment_dict['_id'] = ObjectId()
    comment_dict['user'] = dict(comment_dict['user'])

    # Add comment
    project_response = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id),
            'bugs._id': ObjectId(bug_id)
        },
        {
            '$push': {
                'bugs.$.comments': comment_dict
            }
        },
        return_document=True
    )

    # Serialize and return the project
    updated_project = serialize_project(project_response)
    return updated_project


# Update a comment
@router.put('/projects/{project_id}/bugs/{bug_id}/comments/{comment_id}')
async def update_comment(
    project_id: str,
    bug_id: str,
    comment_id: str,
    comment: CommentUpdate,
    token=Cookie(None)
):
    # Auth user
    auth_user(token)

    comment_dict = dict(comment)

    # Update comment
    project_response = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id),
            'bugs._id': ObjectId(bug_id),
            'bugs.comments._id': ObjectId(comment_id)
        },
        {
            '$set': {
                'bugs.$.comments.$[comment].text': comment_dict['text'],
                'bugs.$.comments.$[comment].updated_at': comment_dict['updated_at']
            }
        },
        {
            'created_at': 0,
            'updated_at': 0
        },
        array_filters=[{'comment._id': ObjectId(comment_id)}],
        return_document=True
    )

    # Serialize and return the project
    updated_project = serialize_project(project_response)
    return updated_project
