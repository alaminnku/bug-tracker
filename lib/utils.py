from pydantic import Field
from datetime import datetime, timezone


# Get utc now
def get_utc_now():
    return datetime.now(timezone.utc)


# Current utc timestamp
utc_now = Field(get_utc_now())


# Serialize comment
def serialize_comment(comment):
    # Format id
    comment['id'] = str(comment.pop('_id'))

    # Return serialized comment
    return comment


# Serialize bug
def serialize_bug(bug):
    # Format id
    bug['id'] = str(bug.pop('_id'))

    # Serialize comments
    serialized_comments = [serialize_comment(
        comment) for comment in bug.get('comments', [])]

    # Update comments
    bug['comments'] = serialized_comments

    # Return serialized bug
    return bug


# Serialize project
def serialize_project(project):
    # Format id
    project['id'] = str(project.pop('_id'))

    # Serialize bugs
    serialized_bugs = [serialize_bug(bug) for bug in project.get('bugs', [])]

    # Update bugs
    project['bugs'] = serialized_bugs

    # Return serialized project
    return project
