from fastapi import APIRouter, Request

router = APIRouter()


# Get a projects bugs
@router.get('/projects/{project_id}/bugs')
async def get_bugs(request: Request):
    return {'message': 'Get bugs'}

# Get a specific bug
@router.get('/projects/{project_id}/bugs/{bug_id}')
async def get_bugs(request: Request):
    return {'message': 'Get a bug'}


# Create a new bug
@router.post('/projects/{project_id}/bugs')
async def get_bugs(request: Request):
    return {'message': 'Create bug'}


# Update a bug
@router.put('/projects/{project_id}/bugs/{bug_id}')
async def get_bugs(request: Request):
    return {'message': 'Update bug'}


