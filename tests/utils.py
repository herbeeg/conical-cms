import json

def register(client, email, username, password):
    return client.post(
        '/register',
        data=json.dumps({
            'email': email,
            'username': username,
            'password': password
        }),
        content_type='application/json'
    )
