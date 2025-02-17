from django.urls import path

from dashboard.views import GetUserProfileView

urlpatterns = [
    path('GetUserProfile/', GetUserProfileView.as_view(), name='get_user_profile' )
]