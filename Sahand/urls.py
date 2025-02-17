"""
URL configuration for Sahand project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from chat.routing import websocket_urlpatterns

urlpatterns = [
    path('', include('home.urls')),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    # Swagger Url
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    # apps
    path('fileManager/', include('file_manager.urls')),
    path('contentManager/', include('content_manager.urls')),
    path('cms/', include('cms.urls')),
    path('activity/', include('activity.urls')),
    path('info/', include('info.urls')),
    path('base/', include('base.urls')),
    path('security/', include('security.urls')),
    path('', include('frontend_api.urls')),
    path('', include('base_api.urls')),
    path('authorize/', include('authorization.urls')),
    path('course/', include('course.urls')),
    path('communicating/', include('communicating.urls')),
    path('taskManager/', include('task_manager.urls')),
    path('chat/', include('chat.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('payment/', include('payment.urls')),

]
