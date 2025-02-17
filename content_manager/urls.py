from django.urls import path
from .views import (
    ContentManagerAddOrUpdateView, ContentManagerGetListView, ContentManagerGetView,
    ContentManagerDeleteView, ContentManagerUndeleteView
)

urlpatterns = [
    # ContentManager URLs
    path('ContentManagerAddOrUpdate/', ContentManagerAddOrUpdateView.as_view(), name="content_manager_add_or_update"),
    path('ContentManagerList/', ContentManagerGetListView.as_view(), name="content_manager_get_list"),
    path('ContentManagerGet/', ContentManagerGetView.as_view(), name="content_manager_get"),
    path('ContentManagerDelete/', ContentManagerDeleteView.as_view(), name="content_manager_delete"),
    path('ContentManagerUndelete/', ContentManagerUndeleteView.as_view(), name="content_manager_undelete"),
]
