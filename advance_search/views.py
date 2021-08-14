from __future__ import unicode_literals
from common import constants
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# import bcrypt
from common.commonFunction import checkSession, getExpires, setCookies
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import urllib
from django.core.paginator import Paginator
from ratelimit import limits
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@csrf_exempt
def login(request):
    cookie = request.COOKIES
    userInfo = checkSession(request)
    if isinstance(userInfo, bool):
        return render(request, constants.LOGIN_PAGE_ADDR, {})

    response = HttpResponseRedirect('users/')

    return setCookies(cookie, response)

@csrf_exempt
def check_user(request, user, password):
    try:
        expires = getExpires(1800) # setting session
        if user == "admin" and password =='admin': # Hardcoded credentials
       
            response = HttpResponse(json.dumps(
                {'success': True, 'status_code': 200, 'user': user}
            ), content_type='application/json')

            response.set_cookie(key='user_session',
                                value=user, expires=expires)

            response.set_cookie(key='user', value=user, expires=expires)
            print(response)
            return response
        else:
            return JsonResponse({'statusMessage': constants.WRONG_PASSWORD, 'status': constants.ERROR_CODE}, status=500, safe=False)

    except Exception as error:
        return JsonResponse({'statusMessage': str(error), 'status': constants.ERROR_CODE}, status=500, safe=False)


@csrf_exempt
def check_cred(request):
    data = json.loads(request.body)
    # print(data)
    username = data['username'].lower()
    password = data['password']
    user_result = check_user(request, username,
                                password)
    return user_result

@csrf_exempt
def advance_search_function(request):
    try:
        if True:
            data = request.GET.copy()
            params = map_request_data(data)
            page = request.GET.get('page',1)
            if not params :
                return render(request, constants.HOME_PAGE_ADDR, {"totalRecords": 0,"result":[],"page":1})
            req = urllib.parse.urlencode(params)
            full_url = constants.STACK_URL+req  # creating url from parameters

            # Checking if data is present in cache
            if full_url in cache:
                cached_url = cache.get(full_url)
                if cached_url :
                    print('cached data')
                    cached_search_result = cached_url
                    # Pagianting the result
                    paginator = Paginator(cached_search_result,10)
                    page_data = paginator.page(page)

                    return render(request, constants.HOME_PAGE_ADDR, {"totalRecords": len(cached_search_result),"result":page_data.object_list,"page":page_data})
            else:
                print('non cached data')
                # call stackoverflow API
                stack_overflow_status = get_stackoverflow_response(full_url)
                if 'items' in stack_overflow_status:
                    # Setting the cache
                    cache.set(full_url, stack_overflow_status['items'], timeout=CACHE_TTL)  
                    # Pagianting the result
                    paginator = Paginator(stack_overflow_status['items'],10)
                    page_data = paginator.page(page)
                    result = {"totalRecords": len(stack_overflow_status['items']),"result": page_data.object_list,"page":page_data}
                    
                    return render(request, constants.HOME_PAGE_ADDR, result)  
                else:
                    return render(request, constants.HOME_PAGE_ADDR, {"result":{},"totalRecords":0}) 
    except Exception as error:
        print("error in advance_search_function() ",error)
        return render(request, constants.HOME_PAGE_ADDR, {"error":error})


@limits(calls=5, period=60)    # Limiting 5 calls a minutes
@limits(calls=100, period=86400)  # Limiting 100 calls a day
def get_stackoverflow_response(full_url):
    stack_overflow_status = requests.get(url = full_url)
    stack_overflow_status = stack_overflow_status.json()
    return stack_overflow_status


def map_request_data(data):
    try:
        params = {}
        if 'page' in data and data['page']:
            params['page'] = data['page']
        if 'pagesize' in data and data['pagesize']:
            params['pagesize'] = data['pagesize']
        if 'fromdate' in data and data['fromdate']:
            params['fromdate'] = data['fromdate']
        if 'todate' in data and data['todate']:
            params['todate'] = data['todate']
        if 'order' in data and data['order']:
            params['order'] = data['order']
        if 'min' in data and data['min']:
            params['min'] = data['min']
        if 'max' in data and data['max']:
            params['max'] = data['max']
        if 'sort' in data and data['sort']:
            params['sort'] = data['sort']
        if 'q' in data and data['q']:
            params['q'] = data['q']
        if 'accepted' in data and data['accepted']:
            params['accepted'] = data['accepted']
        if 'answers' in data and data['answers']:
            params['answers'] = data['answers']
        if 'body' in data and data['body']:
            params['body'] = data['body']
        if 'closed' in data and data['closed']:
            params['closed'] = data['closed']
        if 'migrated' in data and data['migrated']:
            params['migrated'] = data['migrated']
        if 'nottagged' in data and data['nottagged']:
            params['nottagged'] = data['nottagged']
        if 'tagged' in data and data['tagged']:
            params['tagged'] = data['tagged']
        if 'title' in data and data['title']:
            params['title'] = data['title']
        if 'user' in data and data['user']:
            params['user'] = data['user']
        if 'url' in data and data['url']:
            params['url'] = data['url']
        if 'views' in data and data['views']:
            params['views'] = data['views']            
        if 'wiki' in data and data['wiki']:
            params['wiki'] = data['wiki']  
    except Exception as error:
        print("mapping error ",error)
        return False
    return params


# Hadling 500 Errors
def handler500(request):
    return render(request, "Shared/500.html")