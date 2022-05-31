from django.conf import settings
from app.user_session import getUser

def globals(request):
    return {
        'appUser':getUser(request.session)
    }