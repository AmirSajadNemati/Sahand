from django.urls import path
from .views import MessageAddOrUpdateView, MessageGetListView, MessageGetView, MessageDeleteView, MessageUndeleteView, lobby

urlpatterns = [
    path('MessageAddOrUpdate/', MessageAddOrUpdateView.as_view(), name="message_add_or_update"),
    path('MessageList/', MessageGetListView.as_view(), name="message_get_list"),
    path('MessageGet/', MessageGetView.as_view(), name="message_get"),
    path('MessageDelete/', MessageDeleteView.as_view(), name="message_delete"),
    path('MessageUnDelete/', MessageUndeleteView.as_view(), name="message_undelete"),
    path('Group/', lobby)
]
