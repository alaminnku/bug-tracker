from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get('/tasks')
async def get_tasks(request: Request):
    print(request.state.user)
    return {'message': 'Get tasks'}


@router.post('/tasks')
async def create_task(request: Request): 
    print(request.state.user)
    return {'message': 'Create task'}