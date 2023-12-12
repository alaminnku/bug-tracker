from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_projects():
    return {'message': 'Hello world!'}

@app.get('/tasks/{id}')
def get_project(id):
    return {'task': id}
