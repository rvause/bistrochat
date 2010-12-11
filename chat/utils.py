from models import Chatter
from datetime import timedelta


def expired_users(c):
    expiry = timedelta(seconds=30)
    tbr = c.check_in - expiry

    u = Chatter.objects.all()

    for user in u:
        if tbr > user.check_in:
            user.delete()
            
    return u;

