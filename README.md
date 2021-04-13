# social-network
Simple REST API. Django Rest Framework.
___
Python 3.9
Django 3.1
Django REST Framework 3.12
djangorestframework-simplejwt
___

Auth
POST /api/auth nA
POST api/token/refresh/ nA

Register
POST /api/register/ nA

User
GET /api/users nA
GET /api/users/{id} nA

Post
GET /api/posts nA
GET /api/posts/{id} nA
POST /api/posts A
PUT /api/posts/{id}/ A
PATCH /api/posts/{id}/ A
DELETE /api/posts/{id}/ A
*with slash at the end

Like
GET /api/likes nA
GET /api/likes/{id} nA
POST /api/likes A
DELETE /api/likes/{id}/ A
*with slash at the end

Analytics
GET /api/analytics/?date_from=2020-02-02&date_to=2020-02-15 nA

User activity
GET /api/user-activity/ nA
GET /api/user-activity/{id} nA

A - needs authorization
nA - doesn't
