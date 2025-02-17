from django.urls import path
from task_manager.views import (TaskProjectAddOrUpdateView, TaskProjectGetListView, TaskProjectGetView,
                                TaskProjectDeleteView,
                                TaskProjectUndeleteView,
                                TaskDoneAddOrUpdateView, TaskDoneGetListView, TaskDoneGetView,
                                TaskDoneDeleteView,
                                TaskDoneUndeleteView, TaskRequestAddOrUpdateView, TaskRequestGetListView,
                                TaskRequestGetView, TaskRequestDeleteView, TaskRequestUndeleteView,
                                NotificationAddOrUpdateView, NotificationGetListView, NotificationGetView, \
                                NotificationDeleteView, NotificationUndeleteView)
from task_manager.views.task_project_api import IsUserTaskProjectManagerrView
from task_manager.views.task_request_api import MyTasksGetView, TaskRequestNoteListView

urlpatterns = [
    # task_project
    path('TaskProjectAddOrUpdate/', TaskProjectAddOrUpdateView.as_view(), name="task_project_add_or_update"),
    path('TaskProjectList/', TaskProjectGetListView.as_view(), name="task_project_get_list"),
    path('TaskProjectGet/', TaskProjectGetView.as_view(), name="task_project_get"),
    path('TaskProjectDelete/', TaskProjectDeleteView.as_view(), name="task_project_delete"),
    path('TaskProjectUnDelete/', TaskProjectUndeleteView.as_view(), name="task_project_undelete"),
    path('IsUserTaskProjectManagerr/', IsUserTaskProjectManagerrView.as_view(), name="is_user_manager"),

    # task_done
    # path('TaskDoneAddOrUpdate/', TaskDoneAddOrUpdateView.as_view(), name="task_done_add_or_update"),
    # path('TaskDoneList/', TaskDoneGetListView.as_view(), name="task_done_get_list"),
    # path('TaskDoneGet/', TaskDoneGetView.as_view(), name="task_done_get"),
    # path('TaskDoneDelete/', TaskDoneDeleteView.as_view(), name="task_done_delete"),
    # path('TaskDoneUnDelete/', TaskDoneUndeleteView.as_view(), name="task_done_undelete"),

    # task_req
    path('TaskRequestAddOrUpdate/', TaskRequestAddOrUpdateView.as_view(), name="task_req_add_or_update"),
    path('TaskRequestList/', TaskRequestGetListView.as_view(), name="task_req_get_list"),
    path('TaskRequestGet/', TaskRequestGetView.as_view(), name="task_req_get"),
    path('TaskRequestDelete/', TaskRequestDeleteView.as_view(), name="task_req_delete"),
    path('TaskRequestUnDelete/', TaskRequestUndeleteView.as_view(), name="task_req_undelete"),
    path('MyTaskGet/', MyTasksGetView.as_view(), name="get_my_tasks"),
    path('TaskRequestNoteList/', TaskRequestNoteListView.as_view(), name="task_note_list"),

    # notification
    path('NotificationAddOrUpdate/', NotificationAddOrUpdateView.as_view(), name="notification_add_or_update"),
    path('NotificationList/', NotificationGetListView.as_view(), name="notification_get_list"),
    path('NotificationGet/', NotificationGetView.as_view(), name="notification_get"),
    path('NotificationDelete/', NotificationDeleteView.as_view(), name="notification_delete"),
    path('NotificationUnDelete/', NotificationUndeleteView.as_view(), name="notification_undelete"),

]
