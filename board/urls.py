from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list',views.profile_list , name="profile_list"),
    path('profile/<int:pk>',views.profile , name="profile"),
    path('login/',views.login_user , name="login"),
    path('logout/',views.logout_user , name="logout"),
    path('signup/',views.signup_view , name="signup"),
    path('search/',views.search , name="search"),
    path('update_user/',views.update_user , name="update_user"),
    path('edit_image',views.edit_image , name="edit_image"),
]