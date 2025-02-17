from django.urls import path
from course.views import (CourseAddOrUpdateView, CourseGetListView, CourseGetView, CourseDeleteView, CourseUndeleteView,
                          CourseCategoryAddOrUpdateView, CourseCategoryGetListView, CourseCategoryGetView,
                          CourseCategoryDeleteView,
                          CourseCategoryUndeleteView, EpisodeAddOrUpdateView, EpisodeGetListView, EpisodeGetView,
                          EpisodeDeleteView, EpisodeUndeleteView, EpisodeQAAddOrUpdateView, EpisodeQAGetListView,
                          EpisodeQAGetView, EpisodeQADeleteView, EpisodeQAUndeleteView, )





urlpatterns = [
    # course
    path('CourseAddOrUpdate/', CourseAddOrUpdateView.as_view(), name="course_add_or_update"),
    path('CourseList/', CourseGetListView.as_view(), name="course_get_list"),
    path('CourseGet/', CourseGetView.as_view(), name="course_get"),
    path('CourseDelete/', CourseDeleteView.as_view(), name="course_delete"),
    path('CourseUnDelete/', CourseUndeleteView.as_view(), name="course_undelete"),


    # course_category
    path('CourseCategoryAddOrUpdate/', CourseCategoryAddOrUpdateView.as_view(), name="course_category_add_or_update"),
    path('CourseCategoryList/', CourseCategoryGetListView.as_view(), name="course_category_get_list"),
    path('CourseCategoryGet/', CourseCategoryGetView.as_view(), name="course_category_get"),
    path('CourseCategoryDelete/', CourseCategoryDeleteView.as_view(), name="course_category_delete"),
    path('CourseCategoryUnDelete/', CourseCategoryUndeleteView.as_view(), name="course_category_undelete"),

    # episode
    path('EpisodeAddOrUpdate/', EpisodeAddOrUpdateView.as_view(), name="episode_add_or_update"),
    path('EpisodeList/', EpisodeGetListView.as_view(), name="episode_get_list"),
    path('EpisodeGet/', EpisodeGetView.as_view(), name="episode_get"),
    path('EpisodeDelete/', EpisodeDeleteView.as_view(), name="episode_delete"),
    path('EpisodeUnDelete/', EpisodeUndeleteView.as_view(), name="episode_undelete"),

    # episode_qa
    path('EpisodeQAAddOrUpdate/', EpisodeQAAddOrUpdateView.as_view(), name="episode_qa_add_or_update"),
    path('EpisodeQAList/', EpisodeQAGetListView.as_view(), name="episode_qa_get_list"),
    path('EpisodeQAGet/', EpisodeQAGetView.as_view(), name="episode_qa_get"),
    path('EpisodeQADelete/', EpisodeQADeleteView.as_view(), name="episode_qa_delete"),
    path('EpisodeQAUnDelete/', EpisodeQAUndeleteView.as_view(), name="episode_qa_undelete"),
 ]