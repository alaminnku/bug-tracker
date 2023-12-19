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
        'bugs': [serialize_bug(bug) for bug in project.get('bugs', [])],
        **project
    }
    return updated_project


# Serialize bug
def serialize_bug(bug):
    updated_bug = {
        'id': str(bug.pop('_id')),
        'comments': [
            serialize_comment(comment) for comment in bug.get('comments', [])
        ],
        **bug
    }
    return updated_bug


# Serialize comment
def serialize_comment(comment):
    updated_comment = {
        'id': str(comment.pop('_id')),
        **comment
    }
    return updated_comment
