from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings

from django.urls import path, include 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/<int:post_id>", views.update_post, name="update_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("Unfollow", views.Unfollow, name="Unfollow"),
    path("following", views.following, name="following"),
    path("createReview", views.createReview, name="createReview"),
    path("like/<int:post_id>", views.like, name="like"),
    path("restaurantInfo/<int:restaurant_id>", views.restaurantInfo, name="restaurantInfo"),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.png"))),
    path("restaurantProfile/<int:restaurant_id>", views.restaurantProfile, name="restaurantProfile"),
    path("account/<int:user_id>", views.account, name="account"),
    path("update_account", views.update_account, name="update_account"),
    path("new_restaurant", views.new_restaurant, name="new_restaurant"),
    path("dayplanner/<int:restaurant_id>", views.dayplanner, name='dayplanner'),
    path("dayplanner/<int:restaurant_id>/previous", views.previous, name="previous"),
    path("dayplanner/<int:restaurant_id>/next", views.next, name="next"),
    path("dayplanner/new/<int:restaurant_id>", views.event, name="event_new"),
    path("dayplanner/<int:restaurant_id>/edit/<int:event_id>", views.event, name="event_edit"),
]