from django.urls import path
from blog import views


urlpatterns = [
    path('blog/', views.home, name='blog-home'),
    path('userdetail/',views.Signup.as_view()),
    path('signin/',views.Signin.as_view()),
    #path('/',views.user.as_view()),
    
]