from .models import *
from .models import User


def verify_user(path):
    # try to get the user from thepath
    try:
        user =  User.objects.get(pk=path.split("/chat/")[1])
    except:
        return False
    return user.username