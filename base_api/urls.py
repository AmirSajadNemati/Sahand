from django.urls import path
from .views import ShowServerTimeView, GetPanelInfoView, GetAppInfoView, GetAuthorizeInfoView, GetSiteInfoView, \
    SearchPanelMenuView

urlpatterns = [
    path('Main/ServerTime/', ShowServerTimeView.as_view(), name='show_server_time'),
    path('Main/GetPanelInfo/', GetPanelInfoView.as_view(), name='get_panel_info'),
    path('Main/GetAppInfo/', GetAppInfoView.as_view(), name='get_app_info'),
    path('Main/GetAuthorizeInfo/', GetAuthorizeInfoView.as_view(), name='get_auth_info'),
    path('Main/GetSiteInfo/', GetSiteInfoView.as_view(), name='get_site_info'),
    path('Main/SearchPanelMenu/', SearchPanelMenuView.as_view(), name='search_panel_menu')
]
