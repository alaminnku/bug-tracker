def serialize_user (user) -> dict:
    return {
        'id': str(user['_id']),
        'name': str(user['name']),
        'email': str(user['email'])
    }


def serialize_users (users) -> list:
    return [serialize_user(user) for user in users]