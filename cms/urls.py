from django.urls import path

from cms.views import (BlogAddOrUpdateView, BlogGetListView, BlogGetView, BlogDeleteView, BlogUndeleteView,
                       ContentCategoryAddOrUpdateView, ContentCategoryGetListView, ContentCategoryGetView,
                       ContentCategoryDeleteView, ContentCategoryUndeleteView,
                       EventAddOrUpdateView, EventGetListView, EventGetView, EventDeleteView, EventUndeleteView,
                       StoryAddOrUpdateView, StoryGetListView, StoryGetView, StoryDeleteView, StoryUndeleteView,
                       SurveyAddOrUpdateView, SurveyGetListView, SurveyGetView, SurveyDeleteView, SurveyUndeleteView,
                       VideoAddOrUpdateView, VideoGetListView, VideoGetView, VideoDeleteView, VideoUndeleteView,
                       VoiceAddOrUpdateView, VoiceGetListView, VoiceGetView, VoiceDeleteView, VoiceUndeleteView,
                       TopicAddOrUpdateView, TopicGetListView, TopicGetView, TopicDeleteView, TopicUndeleteView,
                       TopicPostAddOrUpdateView, TopicPostGetListView, TopicPostGetView, TopicPostDeleteView,
                       TopicPostUndeleteView,
                       GalleryAddOrUpdateView, GalleryGetListView, GalleryGetView, GalleryDeleteView,
                       GalleryUndeleteView, ServiceAddOrUpdateView, ServiceGetListView, ServiceGetView,
                       ServiceDeleteView, ServiceUndeleteView, BannerAddOrUpdateView, BannerGetListView, BannerGetView,
                       BannerDeleteView, BannerUndeleteView,
                       PostAddOrUpdateView, PostGetListView, PostGetView, PostDeleteView, PostUndeleteView,
                       WorkSampleAddOrUpdateView, WorkSampleGetListView, WorkSampleGetView, WorkSampleDeleteView,
                       WorkSampleUndeleteView, BrandAddOrUpdateView, BrandGetListView, BrandGetView, BrandDeleteView, \
                       BrandUndeleteView
                       )

urlpatterns = [
    # blog
    path('BlogAddOrUpdate/', BlogAddOrUpdateView.as_view(), name="blog_add_or_update"),
    path('BlogList/', BlogGetListView.as_view(), name="blog_get_list"),
    path('BlogGet/', BlogGetView.as_view(), name="blog_get"),
    path('BlogDelete/', BlogDeleteView.as_view(), name="blog_delete"),
    path('BlogUnDelete/', BlogUndeleteView.as_view(), name="blog_undelete"),
    # work sample
    path('WorkSampleAddOrUpdate/', WorkSampleAddOrUpdateView.as_view(), name="work_sample_add_or_update"),
    path('WorkSampleList/', WorkSampleGetListView.as_view(), name="work_sample_get_list"),
    path('WorkSampleGet/', WorkSampleGetView.as_view(), name="work_sample_get"),
    path('WorkSampleDelete/', WorkSampleDeleteView.as_view(), name="work_sample_delete"),
    path('WorkSampleUnDelete/', WorkSampleUndeleteView.as_view(), name="work_sample_undelete"),
    # service
    path('ServiceAddOrUpdate/', ServiceAddOrUpdateView.as_view(), name="service_add_or_update"),
    path('ServiceList/', ServiceGetListView.as_view(), name="service_get_list"),
    path('ServiceGet/', ServiceGetView.as_view(), name="service_get"),
    path('ServiceDelete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('ServiceUnDelete/', ServiceUndeleteView.as_view(), name="service_undelete"),
    # content_category
    path('ContentCategoryAddOrUpdate/', ContentCategoryAddOrUpdateView.as_view(),
         name="content_category_add_or_update"),
    path('ContentCategoryList/', ContentCategoryGetListView.as_view(), name="content_category_get_list"),
    path('ContentCategoryGet/', ContentCategoryGetView.as_view(), name="content_category_get"),
    path('ContentCategoryDelete/', ContentCategoryDeleteView.as_view(), name="content_category_delete"),
    path('ContentCategoryUnDelete/', ContentCategoryUndeleteView.as_view(), name="content_category_undelete"),
    # event
    path('EventAddOrUpdate/', EventAddOrUpdateView.as_view(), name="event_add_or_update"),
    path('EventList/', EventGetListView.as_view(), name="event_get_list"),
    path('EventGet/', EventGetView.as_view(), name="event_get"),
    path('EventDelete/', EventDeleteView.as_view(), name="event_delete"),
    path('EventUnDelete/', EventUndeleteView.as_view(), name="event_undelete"),
    # Story
    path('StoryAddOrUpdate/', StoryAddOrUpdateView.as_view(), name="story_add_or_update"),
    path('StoryList/', StoryGetListView.as_view(), name="story_get_list"),
    path('StoryGet/', StoryGetView.as_view(), name="story_get"),
    path('StoryDelete/', StoryDeleteView.as_view(), name="story_delete"),
    path('StoryUnDelete/', StoryUndeleteView.as_view(), name="story_undelete"),
    # Post
    path('PostAddOrUpdate/', PostAddOrUpdateView.as_view(), name="post_add_or_update"),
    path('PostList/', PostGetListView.as_view(), name="post_get_list"),
    path('PostGet/', PostGetView.as_view(), name="post_get"),
    path('PostDelete/', PostDeleteView.as_view(), name="post_delete"),
    path('PostUnDelete/', PostUndeleteView.as_view(), name="post_undelete"),
    # Post
    path('BannerAddOrUpdate/', BannerAddOrUpdateView.as_view(), name="banner_add_or_update"),
    path('BannerList/', BannerGetListView.as_view(), name="banner_get_list"),
    path('BannerGet/', BannerGetView.as_view(), name="banner_get"),
    path('BannerDelete/', BannerDeleteView.as_view(), name="banner_delete"),
    path('BannerUnDelete/', BannerUndeleteView.as_view(), name="banner_undelete"),
    # survey
    path('SurveyAddOrUpdate/', SurveyAddOrUpdateView.as_view(), name="survey_add_or_update"),
    path('SurveyList/', SurveyGetListView.as_view(), name="survey_get_list"),
    path('SurveyGet/', SurveyGetView.as_view(), name="survey_get"),
    path('SurveyDelete/', SurveyDeleteView.as_view(), name="survey_delete"),
    path('SurveyUnDelete/', SurveyUndeleteView.as_view(), name="survey_undelete"),

    # video
    path('VideoAddOrUpdate/', VideoAddOrUpdateView.as_view(), name="video_add_or_update"),
    path('VideoList/', VideoGetListView.as_view(), name="video_get_list"),
    path('VideoGet/', VideoGetView.as_view(), name="video_get"),
    path('VideoDelete/', VideoDeleteView.as_view(), name="video_delete"),
    path('VideoUnDelete/', VideoUndeleteView.as_view(), name="video_undelete"),

    # voice
    path('VoiceAddOrUpdate/', VoiceAddOrUpdateView.as_view(), name="voice_add_or_update"),
    path('VoiceList/', VoiceGetListView.as_view(), name="voice_get_list"),
    path('VoiceGet/', VoiceGetView.as_view(), name="voice_get"),
    path('VoiceDelete/', VoiceDeleteView.as_view(), name="voice_delete"),
    path('VoiceUnDelete/', VoiceUndeleteView.as_view(), name="voice_undelete"),

    # topic
    path('TopicAddOrUpdate/', TopicAddOrUpdateView.as_view(), name="topic_add_or_update"),
    path('TopicList/', TopicGetListView.as_view(), name="topic_get_list"),
    path('TopicGet/', TopicGetView.as_view(), name="topic_get"),
    path('TopicDelete/', TopicDeleteView.as_view(), name="topic_delete"),
    path('TopicUnDelete/', TopicUndeleteView.as_view(), name="topic_undelete"),

    # topic_post
    path('TopicPostAddOrUpdate/', TopicPostAddOrUpdateView.as_view(), name="topic_post_add_or_update"),
    path('TopicPostList/', TopicPostGetListView.as_view(), name="topic_post_get_list"),
    path('TopicPostGet/', TopicPostGetView.as_view(), name="topic_post_get"),
    path('TopicPostDelete/', TopicPostDeleteView.as_view(), name="topic_post_delete"),
    path('TopicPostUnDelete/', TopicPostUndeleteView.as_view(), name="topic_post_undelete"),
    # Gallery
    path('GalleryAddOrUpdate/', GalleryAddOrUpdateView.as_view(), name="gallery_add_or_update"),
    path('GalleryList/', GalleryGetListView.as_view(), name="gallery_get_list"),
    path('GalleryGet/', GalleryGetView.as_view(), name="gallery_get"),
    path('GalleryDelete/', GalleryDeleteView.as_view(), name="gallery_delete"),
    path('GalleryUnDelete/', GalleryUndeleteView.as_view(), name="gallery_undelete"),

    # brand
    path('BrandAddOrUpdate/', BrandAddOrUpdateView.as_view(), name="brand_add_or_update"),
    path('BrandList/', BrandGetListView.as_view(), name="brand_get_list"),
    path('BrandGet/', BrandGetView.as_view(), name="brand_get"),
    path('BrandDelete/', BrandDeleteView.as_view(), name="brand_delete"),
    path('BrandUnDelete/', BrandUndeleteView.as_view(), name="brand_undelete"),


]
