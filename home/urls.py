from . import views
from django.urls import path

urlpatterns = [
    # path('login', views.phone_entry_view, name='phone_entry'),
    path('sms-code-entry/', views.sms_code_entry_view, name='sms_code_entry'),
    path('', views.loginUser, name="login"),
    path("logout/", views.LogOutView, name='log_out'),
    # path('AddUser/', views.AddBlogView.as_view()),
    # path('AddUser1/', views.AddBlogView1.as_view()),
]