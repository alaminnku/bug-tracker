from fastapi import APIRouter
from config.db import db
from bson import ObjectId
from models.projects import Comment

router = APIRouter()


# Get all comments
@router.get('/projects/{project_id}/bugs/{bug_id}/comments')
async def get_comments(project_id: str, bug_id: str):
    # Get the project
    project = db.projects.find_one({'_id': ObjectId(project_id)})

    # Get the bug
    bug = next((bug for bug in project['bugs']
               if str(bug['_id'] == bug_id)), None)

    # Convert comment ObjectId to id
    comments = [
        {
            'id': str(comment.pop('_id')),
            **comment
        } for comment in bug['comments']]

    # Return comments
    return comments


# Create a new comment
@router.post('/projects/{project_id}/bugs/{bug_id}/comments')
async def create_comment(project_id: str, bug_id: str, comment: Comment):
    # Convert model to dict
    comment_dict = dict(comment)
    comment_dict['_id'] = ObjectId()
    comment_dict['user'] = dict(comment_dict['user'])

    # Add comment
    updated_project = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id),
            'bugs._id': ObjectId(bug_id)
        },
        {
            '$push': {
                'bugs.$.comments': comment_dict
            }
        }, return_document=True)

    # Convert ObjectId to id
    updated_project['id'] = str(updated_project.pop('_id'))
    updated_project['bugs'] = [
        {
            'id': str(bug.pop('_id')),
            'comments': [
                {
                    'id': str(project_comment.pop('_id')), **project_comment
                } for project_comment in bug['comments']],
            **bug
        } for bug in updated_project['bugs']]

    # Return the project
    return updated_project


# Update a comment
@router.put('/projects/{project_id}/bugs/{bug_id}/comments/{comment_id}')
async def update_comment(project_id: str, bug_id: str, comment_id: str, text: str):
    # Update comment
    updated_project = db.projects.find_one_and_update(
        {
            '_id': ObjectId(project_id),
            'bugs._id': ObjectId(bug_id),
            'bugs.comments._id': ObjectId(comment_id)
        },
        {
            '$set': {
                'bugs.$.comments.$[comment].text': text
            }
        },
        array_filters=[{'comment._id': ObjectId(comment_id)}],
        return_document=True
    )

    # Convert ObjectId to id
    updated_project['id'] = str(updated_project.pop('_id'))
    updated_project['bugs'] = [
        {
            'id': str(bug.pop('_id')),
            'comments': [
                {
                    'id': str(comment.pop('_id')),
                    **comment
                } for comment in bug['comments']],
            **bug
        } for bug in updated_project['bugs']
    ]

    # Return updated project
    return updated_project
