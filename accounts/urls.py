from django.urls import path
from accounts import views
from django.conf.urls import include

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='account_signup'),
	path('login/', views.LoginView.as_view(), name='account_login'),
	path('logout/', views.LogoutView.as_view(), name='account_logout'),
]