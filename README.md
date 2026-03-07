Instagram Clone (Django + WebSockets)

A simplified Instagram Clone built using Django, Django REST Framework, PostgreSQL, and WebSockets (Django Channels) with a basic frontend using HTML, CSS, and JavaScript.

This project was created as a technical assignment to demonstrate backend API development, real-time communication, and frontend integration.


Features
User & Posts

Create posts with image and caption

View posts in feed

Display username and caption

Likes

Like / Unlike posts

Double-tap like animation ❤️

Like count per post

Comments

Add comments

Display username with comment

Delete comments

Stories

Upload stories

Stories expire after 24 hours

Instagram-style story circles UI

Real-time Chat

WebSocket chat using Django Channels

Messages appear instantly without refreshing

Shows sender username

Tech Stack
Backend

Python

Django

Django REST Framework

Django Channels (WebSockets)

PostgreSQL

Frontend

HTML

CSS

JavaScript (Fetch API)

Database

PostgreSQL

Project Structure
insta_clone/
│
├── insta_clone/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│
├── posts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── consumers.py
│   ├── urls.py
│
├── templates/
│   └── posts/
│       └── index.html
│
├── media/
│
└── manage.py
Setup Instructions
1 Install dependencies
pip install django
pip install djangorestframework
pip install psycopg2
pip install channels
2 Configure PostgreSQL

Update settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram_clone',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
3 Run migrations
python manage.py makemigrations
python manage.py migrate
4 Create admin user
python manage.py createsuperuser
5 Start server
python manage.py runserver

Open:

http://127.0.0.1:8000
API Endpoints
Endpoint	Description
/api/posts/	Create & list posts
/api/stories/	Upload and list stories
/api/comments/	Create & list comments
/api/comments/delete/<id>/	Delete comment
/api/like/	Toggle like
/ws/chat/	WebSocket chat
Demo Flow

Create a post with image

Like the post

Add a comment

Delete a comment

Upload a story

Open two browser tabs and test real-time chat

Possible Improvements

Future improvements could include:

User authentication system

Follow / unfollow feature

Notifications

Direct messages

Mobile responsive UI

Production deployment

Author

Vishnu
Python Backend Developer
