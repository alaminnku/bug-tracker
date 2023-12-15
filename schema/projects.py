def serialize_project(project) -> dict:
    return {
        'name': project['name'],
        'description': project['description'],
        'start_date': project['start_date'],
        'end_date': project['end_date'],
        'members': project['members'],
    }


def serialize_projects(projects) -> list:
    return [serialize_project(project) for project in projects]