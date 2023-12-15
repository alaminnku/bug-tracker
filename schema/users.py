def serialize_user (user) -> dict:
    return {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email']
    }


def serialize_users (users) -> list:
    return [serialize_user(user) for user in users]