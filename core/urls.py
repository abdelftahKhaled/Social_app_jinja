from django.urls import path
from .  import views

urlpatterns = [
    path("",views.home,name='home'),
    path("register",views.registere,name='register'),
    path("login",views.sign_in ,name='login'),
    path("logout",views.logout,name='logout'),
    path("setting",views.setting,name='setting'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow',views.follow,name='follow'),
    path('like_post/<str:pk>',views.like_post,name='like_post'),
   
]