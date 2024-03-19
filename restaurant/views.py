import json
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from django.views import generic
from django.utils.safestring import mark_safe
from django.views.generic import View

from .models import User, Post, Category, Follow, Restaurant, Profile, Event
from .utils import Calendar
import calendar
from calendar import HTMLCalendar
from .forms import EventForm

# Create your views here.


def index(request):
    # Return all posts in reverse chronologial order
    posts = Post.objects.all().order_by("-id")
    # it can also be written as
    # posts = Post.objects.all().order_by("id").reverse()

    # creating a paginator object to display 10 items per page
    p = Paginator(posts, 10)

    # getting the desired page number from url
    page_number = request.GET.get('page')
    if page_number == None:
        current_page = 1
    else:
        current_page = int(page_number)
    

    try:
        # returns the desired page object
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integear then assing the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    return render(request, "restaurant/index.html", {
        "page_obj": page_obj,
        "current_page": current_page,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "restaurant/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "restaurant/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "restaurant/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "restaurant/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "restaurant/register.html")

def profile(request, user_id):
    posts = Post.objects.filter(user=user_id).order_by("id").reverse()

    # creating a paginator object to display 10 items per page
    p = Paginator(posts, 10)
    print(p.page_range)

    # getting the desired page number from url
    page_number = request.GET.get('page')
    if page_number == None:
        current_page = 1
    else:
        current_page = int(page_number)


    try:
        # returns the desired page object
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integear then assing the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    user = User.objects.get(pk=user_id)

    # get count() for following and followers
    followers = Follow.objects.filter(poster_follower=user.id).count()
    # print(f"followers : {followers}")
    following = Follow.objects.filter(poster=user.id).count()
    # print(f"following : {following}")

    try:
        followOrNot = Follow.objects.filter(poster_follower=user.id).filter(poster=request.user.id)

        if len(followOrNot) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    foodie = User.objects.get(pk=user_id)


    return render(request, "restaurant/profile.html", {
        "posts": posts,
        "page_obj": page_obj,
        "username": user.username,
        "foodie": foodie,
        "followers": followers,
        "following": following,
        "isFollowing": isFollowing,
        "current_page": current_page,
    })

def follow(request):
    if request.method == "POST":
        poster = User.objects.get(pk=request.user.id)
        print(poster)
        
        poster_follower = request.POST["follow"]
        print(poster_follower)

        poster_follower_sql = User.objects.get(username=poster_follower)
        follow = Follow(poster=poster, poster_follower=poster_follower_sql)
        follow.save()

        user_id = poster_follower_sql.id

        return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id})) 

def Unfollow(request):
    if request.method == "POST":
        poster = User.objects.get(pk=request.user.id)
        print(poster)
        
        poster_follower = request.POST["Unfollow"]
        print(poster_follower)

        poster_follower_sql = User.objects.get(username=poster_follower)
        unfollow = Follow.objects.get(poster=poster, poster_follower=poster_follower_sql)
        unfollow.delete()

        user_id = poster_follower_sql.id

        return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id})) 
    return


def following(request):

    posts = Post.objects.all().order_by("-id")

    try:
    
        current_user = User.objects.get(pk=request.user.id)

        print(current_user)

        posters = Follow.objects.filter(poster=current_user)

        limited_posts = []

        for post in posts:
            for poster in posters:
                if post.user == poster.poster_follower:
                    limited_posts.append(post)

        # creating a paginator object to display 10 items per page
        p = Paginator(limited_posts, 10)
        print(p.page_range)

        # getting the desired page number from url
        page_number = request.GET.get('page')
        if page_number == None:
            current_page = 1
        else:
            current_page = int(page_number)

        try:
            # returns the desired page object
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            # if page_number is not an integear then assing the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        

        return render(request, "restaurant/following.html", {
            "page_obj": page_obj,
            "current_page": current_page,
        })
    
    except User.DoesNotExist:
        return render(request, "restaurant/login.html")
    
@csrf_exempt
@login_required
def createReview(request):

    # Create a new post via POST
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        restaurants = Restaurant.objects.all()
        try:
            id = request.POST["id"]
        except MultiValueDictKeyError:
            return render(request, "restaurant/writeareview.html", {
                "restaurants": restaurants,
                "message": "Invalid restaurant and/or content."
            })
        
        content = request.POST['content']
        restaurant = Restaurant.objects.get(pk=id)
        # Create a post
        post = Post(
            user = user,
            restaurant = restaurant,
            content = content
        )
        post.save()

        return HttpResponseRedirect(reverse(index))
    
    else:
        restaurants = Restaurant.objects.all()
        return render(request, "restaurant/writeareview.html", {
            "restaurants": restaurants
        })
    
@csrf_exempt
@login_required
def update_post(request, post_id):

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get original post using post_id
    post = Post.objects.get(pk=post_id)

    # get edited content in JSON
    data = json.loads(request.body)
    #print(f"data: {data}")
    content = data.get("content","")
    print(content)

    # update post's content
    post.content = content
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)

@csrf_exempt
@login_required    
def restaurantInfo(request, restaurant_id):
    # objects.filter() returns a queryset. it is iterable.
    # objects.get() return a single object. it is not iterable. 
    restaurants = Restaurant.objects.filter(pk=restaurant_id)
    for restaurant in restaurants:
        print(f"restaurant Info: {restaurant.name}")
        # return JsonResponse([restaurant.serialize() for restaurant in restaurants], safe=False)
        return JsonResponse({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
        })

@csrf_exempt
@login_required
def like(request, post_id):

    current_user = User.objects.get(pk=request.user.id)
    # current_user_likes = current_user.likes.all()
    # print(current_user_likes)

    post = Post.objects.get(pk=post_id)

    # remove like if already liked
    if current_user in post.like.all():
        post.like.remove(current_user)
        return JsonResponse({"message": "Post unliked"})

    # add like if not already like
    else:
        post.like.add(current_user)
        return JsonResponse({"message": "Post liked"})

@csrf_exempt
@login_required
def restaurantProfile(request, restaurant_id):
    posts = Post.objects.filter(restaurant=restaurant_id).order_by("id").reverse()

    # creating a paginator object to display 10 items per page
    p = Paginator(posts, 10)
    print(p.page_range)

    # getting the desired page number from url
    page_number = request.GET.get('page')
    if page_number == None:
        current_page = 1
    else:
        current_page = int(page_number)


    try:
        # returns the desired page object
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integear then assing the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    restaurant = Restaurant.objects.get(pk=restaurant_id)
    #print(restaurant.address)

    geolocator = Nominatim(user_agent="restaurant")
    restaurant_address = geolocator.geocode(restaurant.address, timeout=200)
    
    #print(f"restaurant geolocation is {restaurant_address.latitude} and {restaurant_address.longitude}")


    return render(request, "restaurant/restaurantprofile.html", {
        "posts": posts,
        "page_obj": page_obj,
        "restaurant": restaurant,
        "current_page": current_page,
        "restaurant_address":restaurant_address,
    })

@csrf_exempt
@login_required
def account(request, user_id):
    account = User.objects.get(pk=user_id)
    #print(account.profile)

    return render(request, "restaurant/account.html", {
        "account": account,
    })

@csrf_exempt
@login_required
def update_account(request):
    account = User.objects.get(pk=request.user.id)

    # Update Profile via POST
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        name = request.POST['username']
        phone = request.POST['phone']
        try:
            profile_pic = request.FILES['myfile']
        except MultiValueDictKeyError:
            return render(request, "restaurant/account.html", {
                "account": account,
                "message": "Invalid name/phone/profile picture",
            })
        
        # Create a profile instance
        profile = Profile(
            user = user,
            name = name,
            phone = phone,
            profile_pic = profile_pic
        )
        profile.save()

        return HttpResponseRedirect(reverse(index))
    
@csrf_exempt
@login_required
def new_restaurant(request):

    # Create a new post via POST
    if request.method == "POST":
        
        category_id = request.POST['category']
        category = Category.objects.get(pk=category_id)
        name = request.POST['name']
        address = request.POST['address']

        # Create a restaurant
        restaurant = Restaurant(
            category = category,
            name = name,
            address = address
        )
        restaurant.save()

        return HttpResponseRedirect(reverse(index))
    
    else:
        categories = Category.objects.all()
        return render(request, "restaurant/newrestaurant.html", {
            "categories": categories
        })

@csrf_exempt
@login_required
class CalendarView(generic.ListView):
    model = Event
    template_name = 'restaurant/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        #print(d.month)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # events = Event.objects.filter(start_time__year=d.year, start_time__month=d.month)[0]
        # print(f"Events are {events.start_time}")

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(d.year, d.month, withyear=True)
        #print(html_cal)
        context['calendar'] = mark_safe(html_cal)
        return context
        
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.today()

@csrf_exempt
@login_required
def dayplanner(request, restaurant_id, year=datetime.now().year, month=datetime.now().strftime('%B'), day=datetime.now().strftime('%A')):    
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    # Capitalize the title
    month = month.title()
    
    # Shows the month number
    month_number = list(calendar.month_name).index(month)
    #print(month_number)

    cal = Calendar(year, month_number)

    # This is the Calendar object
    html_cal = cal.formatmonth(year, month_number, restaurant_id, request.user.id, withyear=True)

    # Generate links to each day in the calendar
    day_links = ''
    for day_number in range(1, calendar.monthrange(year, month_number)[1] + 1):
        day_links += f'<a href="/{year}/{month}/{day_number}/">{day_number}</a> '

    # Shows the current date
    now = datetime.now()
    
    return render(request, "restaurant/calendar.html", {
        "cal": html_cal,
        "restaurant_id": restaurant_id,
        "restaurant": restaurant,
    })

def previous(request, restaurant_id):
    today = datetime.now()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    print(last_month.strftime("%Y%m"))
    return dayplanner(request, restaurant_id, last_month.year, last_month.strftime("%B"), last_month.strftime("%A"))

def next(request, restaurant_id):
    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    #print(f"days in a month{days_in_month}")
    last = today.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    #print(next_month.strftime("%Y%m"))
    return dayplanner(request, restaurant_id, next_month.year, next_month.strftime("%B"), next_month.strftime("%A"))

@csrf_exempt
@login_required
def event(request, restaurant_id, event_id=None):
    customer = request.user
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id, customer=customer, eatery=restaurant)
    else:
        instance = Event(customer=customer, eatery=restaurant)

    form = EventForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()

        restaurant = request.POST["eatery"]
        restaurant_id = int(restaurant)

        return HttpResponseRedirect(reverse('dayplanner', kwargs={'restaurant_id': restaurant_id}))
    return render(request, 'restaurant/event.html', {
        'form': form,
        'restaurant_id': restaurant_id,
        'restaurant': restaurant,
    })

