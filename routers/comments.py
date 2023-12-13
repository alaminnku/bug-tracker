from fastapi import APIRouter, Request

router = APIRouter()


# Get all comments
@router.get('/projects/{project_id}/bugs/{bug_id}/comments')
async def get_bugs(request: Request, project_id, bug_id):
    return {'message': 'Get all comments'}


# Create a new comment
@router.post('/projects/{project_id}/bugs/{bug_id}/comments')
async def get_bugs(request: Request, project_id, bug_id):
    return {'message': 'Create comment'}


# Update a comment
@router.put('/projects/{project_id}/bugs/{bug_id}/comments/{comment_id}')
async def get_bugs(request: Request, project_id, bug_id, comment_id):
    return {'message': 'Update user'}

