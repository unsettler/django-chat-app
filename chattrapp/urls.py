from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="homeurl"),
    path('accounts/login', views.login_view, name="loginurl"),
    path('logout', views.logout_view, name="logouturl"),
    path('accounts/signup', views.signup_view, name="signupurl"),
    path('resetpassword', views.resetPassword_view, name="reseturl"),
    path('toreset', views.toreset_view, name="toreseturl"),
    path('profileupload', views.profileupload_view, name="profileuploadurl"),
    path('search', views.search_view, name="searchurl"),
    path('display', views.display_view, name="displayurl"),
    path('chat/<int:recipient_id>/', views.chat_view, name='chaturl'),
    path('deleteuser', views.delete_view, name='deleteurl'),
]
