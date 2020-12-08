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

def login(client, username, password):
    return client.post(
        '/login',
        data=json.dumps({
            'username': username,
            'password': password
        }),
        content_type='application/json'
    )

def logout(client):
    return client.get(
        '/logout',
        follow_redirects=False
    )
