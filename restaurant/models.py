from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default="profile.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.name}"

class Category(models.Model):
    categoryType = models.CharField(max_length=64)

    # a function that provides instructions for how to turn a category object into a string in terminal output
    def __str__(self):
        return f"{self.id}: {self.categoryType}"
    
class Restaurant(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    name = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=200, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")

    def __str__(self):
        return f"{self.id}: {self.name} is located at {self.address}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
    
class Follow(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster_follows")
    poster_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")

    def __str__(self):
        return f"{self.poster} is following {self.poster_follower}"

class Event(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    eatery = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="eatery")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        start = timezone.localtime(self.start_time)
        end = timezone.localtime(self.end_time)
        return f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')} {self.customer.profile.name} made a reservation"
    
    @property
    def get_html_url(self):
        url =reverse('event_edit', args=(self.eatery.id, self.id,))
        return f'<a href="{url}"> {self} </a>'
    