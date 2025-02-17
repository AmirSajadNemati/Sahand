from django.urls import path

from activity.views import (CommentAddOrUpdateView, CommentGetListView, CommentGetView, CommentDeleteView,
                            CommentUndeleteView,
                            ItemOperationAddOrUpdateView, ItemOperationGetListView, ItemOperationGetView,
                            ItemOperationDeleteView, ItemOperationUndeleteView,
                            RevisionAddOrUpdateView, RevisionGetListView, RevisionGetView, RevisionDeleteView,
                            RevisionUndeleteView,
                            UserLogAddOrUpdateView, UserLogGetListView, UserLogGetView, UserLogDeleteView,
                            UserLogUndeleteView,
                            UserSurveyAddOrUpdateView, UserSurveyGetListView, UserSurveyGetView, UserSurveyDeleteView,
                            UserSurveyUndeleteView)
from security.views.user_log_api import UserLogListApiView

urlpatterns = [
    # Comment
    path('CommentAddOrUpdate/', CommentAddOrUpdateView.as_view(), name="comment_add_or_update"),
    path('CommentList/', CommentGetListView.as_view(), name="comment_get_list"),
    path('CommentGet/', CommentGetView.as_view(), name="comment_get"),
    path('CommentDelete/', CommentDeleteView.as_view(), name="comment_delete"),
    path('CommentUnDelete/', CommentUndeleteView.as_view(), name="comment_undelete"),

    # ItemOperation
    path('ItemOperationAddOrUpdate/', ItemOperationAddOrUpdateView.as_view(), name="item_operation_add_or_update"),
    path('ItemOperationList/', ItemOperationGetListView.as_view(), name="item_operation_get_list"),
    path('ItemOperationGet/', ItemOperationGetView.as_view(), name="item_operation_get"),
    path('ItemOperationDelete/', ItemOperationDeleteView.as_view(), name="item_operation_delete"),
    path('ItemOperationUnDelete/', ItemOperationUndeleteView.as_view(), name="item_operation_undelete"),

    # Revision
    path('RevisionAddOrUpdate/', RevisionAddOrUpdateView.as_view(), name="revision_add_or_update"),
    path('RevisionList/', RevisionGetListView.as_view(), name="revision_get_list"),
    path('RevisionGet/', RevisionGetView.as_view(), name="revision_get"),
    path('RevisionDelete/', RevisionDeleteView.as_view(), name="revision_delete"),
    path('RevisionUnDelete/', RevisionUndeleteView.as_view(), name="revision_undelete"),

    # UserLog
    # path('UserLogAddOrUpdate/', UserLogAddOrUpdateView.as_view(), name="user_log_add_or_update"),
    # path('UserLogList/', UserLogGetListView.as_view(), name="user_log_get_list"),
    # path('UserLogGet/', UserLogGetView.as_view(), name="user_log_get"),
    # path('UserLogDelete/', UserLogDeleteView.as_view(), name="user_log_delete"),
    # path('UserLogUnDelete/', UserLogUndeleteView.as_view(), name="user_log_undelete"),

    # UserSurvey
    path('UserSurveyAddOrUpdate/', UserSurveyAddOrUpdateView.as_view(), name="user_survey_add_or_update"),
    path('UserSurveyList/', UserSurveyGetListView.as_view(), name="user_survey_get_list"),
    path('UserSurveyGet/', UserSurveyGetView.as_view(), name="user_survey_get"),
    path('UserSurveyDelete/', UserSurveyDeleteView.as_view(), name="user_survey_delete"),
    path('UserSurveyUnDelete/', UserSurveyUndeleteView.as_view(), name="user_survey_undelete"),



]
