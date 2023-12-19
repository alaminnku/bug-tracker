from pydantic import Field
from datetime import datetime, timezone


# Get utc now
def get_utc_now():
    return datetime.now(timezone.utc)


# Current utc timestamp
utc_now = Field(get_utc_now())


# Serialize project
def serialize_project(project):
    updated_project = {
        'id': str(project.pop('_id')),
        'bugs': [
            {
                'id': str(bug.pop('_id')),
                'comments': [
                    {
                        'id': str(comment.pop('_id')),
                        **comment
                    } for comment in bug.get('comments', [])
                ],
                **bug
            } for bug in project.get('bugs', [])],
        **project
    }

    return updated_project
