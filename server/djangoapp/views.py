import json
import requests
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

@csrf_exempt
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
        user = authenticate(username=data.get('userName'), password=data.get('password'))
    except (ValueError, TypeError):
        return JsonResponse({'error':'Invalid JSON'}, status=400)
    if user is None:
        return JsonResponse({'status':'Unauthorized'}, status=401)
    login(request, user)
    return JsonResponse({'userName':user.username, 'status':'Authenticated', 'firstName':user.first_name, 'lastName':user.last_name})

@require_GET
def logout_request(request):
    logout(request)
    return JsonResponse({'userName':'', 'status':'Logged out'})

@csrf_exempt
@require_POST
def registration(request):
    try:
        data = json.loads(request.body)
        username = data['userName'].strip()
        if not username or len(data['password']) < 8:
            return JsonResponse({'error':'Username and password of at least 8 characters required'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error':'Username already exists'}, status=409)
        user = User.objects.create_user(username=username, password=data['password'], first_name=data['firstName'], last_name=data['lastName'], email=data['email'])
        login(request, user)
        return JsonResponse({'status':'Authenticated', 'userName':user.username, 'firstName':user.first_name, 'lastName':user.last_name}, status=201)
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'error':'All five registration fields are required'}, status=400)

def get_dealerships(request, state='All'):
    try:
        endpoint = 'fetchDealers' if state == 'All' else 'fetchDealers/' + state
        return JsonResponse({'status':200, 'dealers':get_request(endpoint)})
    except requests.RequestException:
        return JsonResponse({'error':'Dealership service unavailable'}, status=503)

def get_dealer_details(request, dealer_id):
    try:
        return JsonResponse({'status':200, 'dealer':get_request(f'fetchDealer/{dealer_id}')})
    except requests.RequestException:
        return JsonResponse({'error':'Dealership service unavailable'}, status=503)

def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f'fetchReviews/dealer/{dealer_id}')
        for review in reviews:
            review.update(analyze_review_sentiments(review['review']))
        return JsonResponse({'status':200, 'reviews':reviews})
    except requests.RequestException:
        return JsonResponse({'error':'Review service unavailable'}, status=503)

def get_cars(request):
    cars = [{'CarMake':c.car_make.name, 'CarModel':c.name, 'CarYear':c.year, 'type':c.type} for c in CarModel.objects.select_related('car_make').all()]
    return JsonResponse({'status':200, 'CarMakes':list(CarMake.objects.values('id','name','description')), 'CarModels':cars})

@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'Please log in'}, status=401)
    try:
        data = json.loads(request.body)
        if not str(data.get('review','')).strip():
            return JsonResponse({'error':'Review text is required'}, status=400)
        data['dealership'] = int(data['dealership'])
        data['name'] = request.user.get_full_name() or request.user.username
        saved = post_review(data)
        return JsonResponse({'status':200, 'review':saved})
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'error':'Invalid review'}, status=400)
    except requests.RequestException:
        return JsonResponse({'error':'Review service unavailable'}, status=503)
