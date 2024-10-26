from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

api_01 = FastAPI()

users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]

@api_01.get('/')
def get_index():
    return 'Bonjour à toi, visiteuse/visiteur'

@api_01.get('/users')
def get_users():
    return users_db

@api_01.get('/users/{userid:int}')
def get_user(userid):
    try:
        user = list(filter(lambda u: u.get('user_id') == userid, users_db))[0]
        return user
    except IndexError:
        return {}

@api_01.get('/users/{userid:int}/name')
def get_user_name(userid):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'name': user['name']}
    except IndexError:
        return {}

@api_01.get('/users/{userid:int}/subscription')
def get_user_subscription(userid):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'subscription': user['subscription']}
    except IndexError:
        return {}


class User(BaseModel):
    userid: Optional[int]=None
    name: str
    subscription: str


@api_01.post('/users')
def post_users(user: User):
    new_id = max(users_db, key=lambda u: u.get('user_id'))['user_id']
    new_user = {
        'user_id': new_id + 1,
        'name': user.name,
        'subscription': user.subscription
    }
    users_db.append(new_user)
    return new_user

# # new user curl
# curl -X 'POST' -i \
#   'http://127.0.0.1:8000/users' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "name": "Toto",
#   "subscription": "platine tier"
# }'

@api_01.put('/users/{userid:int}')
def put_users(user: User, userid):
    try:
        old_user = list(filter(lambda u: u.get('user_id') == userid, users_db))[0]
        users_db.remove(old_user)

        old_user['name'] = user.name
        old_user['subscription'] = user.subscription

        users_db.append(old_user)
        return old_user

    except IndexError:
        return 'ID unknown'

# # update user curl
# curl -X 'PUT' -i \
#   'http://127.0.0.1:8000/users/4' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "user_id": 1,
#   "name": "Titi",
#   "subscription": "platine tier"
# }'

@api_01.delete('/users/{userid:int}')
def delete_users(userid):
    try:
        old_user = list(filter(lambda u: u.get('user_id') == userid, users_db))[0]
        users_db.remove(old_user) 

        return 'Deletion done'
    except IndexError:
        return 'ID unknown'

# delete user curl
# curl -X 'DELETE' -i \
#   'http://127.0.0.1:8000/users/1' \
#   -H 'Content-Type: application/json'