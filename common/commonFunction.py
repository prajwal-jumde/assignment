from advance_search.models import *
from datetime import datetime, timedelta
from common import constants
import json
from django.http import HttpResponse
from django.shortcuts import render


def checkSession(request):
    ''' 
    Check for user session in the request.

    Author  : Vaibhav Gupta

    Args:
        request (request object, required) : request body which have cookie of the session.

    Returns:
        if session present then dictionary containing the full_name and user_name of the logged in user.
        else returns False
    '''
    try:
        cookie = request.COOKIES

        user = Users.objects.get(user_name=cookie['user_session'])
        return {"user_name": user.user_name}
    except:
        return False


def getExpires(seconds):
    return datetime.now() + timedelta(seconds=seconds)


def setCookies(cookie, response):
    expires = getExpires(constants.EXPIRES_IN_SECOND)

    if 'user_session' in cookie:
        response.set_cookie(key='user_session',
                            value=cookie['user_session'], expires=expires)
    if 'user_full_name' in cookie:
        response.set_cookie(key='user_full_name',
                            value=cookie['user_full_name'], expires=expires)
    if 'user' in cookie:
        response.set_cookie(key='user', value=cookie['user'], expires=expires)
    if 'storeId' in cookie:
        response.set_cookie(
            key='storeId', value=cookie['storeId'], expires=expires)

    return response
