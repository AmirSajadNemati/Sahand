from django.urls import path
from security.views import (UserAddOrUpdateView, UserGetListView, UserGetView, UserDeleteView,
                            UserUndeleteView, RoleAddOrUpdateView, RoleGetListView, RoleGetView, RoleDeleteView,
                            RoleUndeleteView, OperationAddOrUpdateView, OperationGetListView, OperationGetView,
                            OperationDeleteView,
                            OperationUndeleteView, StaticOperationGetListView)
from security.views.user_log_api import UserLogListApiView

urlpatterns = [
    # User
    path('UserAddOrUpdate/', UserAddOrUpdateView.as_view(), name="user_add_or_update"),
    path('UserList/', UserGetListView.as_view(), name="user_get_list"),
    path('UserGet/', UserGetView.as_view(), name="user_get"),
    path('UserDelete/', UserDeleteView.as_view(), name="user_delete"),
    path('UserUnDelete/', UserUndeleteView.as_view(), name="user_undelete"),

    # Role
    path('RoleAddOrUpdate/', RoleAddOrUpdateView.as_view(), name="role_add_or_update"),
    path('RoleList/', RoleGetListView.as_view(), name="role_get_list"),
    path('RoleGet/', RoleGetView.as_view(), name="role_get"),
    path('RoleDelete/', RoleDeleteView.as_view(), name="role_delete"),
    path('RoleUnDelete/', RoleUndeleteView.as_view(), name="role_undelete"),

    # Operation URLs
    path('OperationAddOrUpdate/', OperationAddOrUpdateView.as_view(), name="operation_add_or_update"),
    path('OperationList/', OperationGetListView.as_view(), name="operation_get_list"),
    path('OperationGet/', OperationGetView.as_view(), name="operation_get"),
    path('OperationDelete/', OperationDeleteView.as_view(), name="operation_delete"),
    path('OperationUndelete/', OperationUndeleteView.as_view(), name="operation_undelete"),

    # StaticOperation
    path('StaticOperationList/', StaticOperationGetListView.as_view(), name="static_operation_get_list"),

    # UserLog
    path('userLogList/', UserLogListApiView.as_view(), name="user_log_list")

]
