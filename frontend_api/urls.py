from django.urls import path
from frontend_api.views import BlogSearchView, BlogListPagination, ContactInfoView, BlogFilterView, ServiceDetailView, \
    TaskRequestDetailView
from frontend_api.views.cms_page_api import BlogDetailView, IndexAPIView, BasePageDetailView, PostDetailView, \
    PostSearchView, WorkSampleSearchView, WorkSampleDetailView, ServiceSearchView, AboutUsDetailView, WhyUsDetailView, \
    StoryListView, WhyUsSearchView
from frontend_api.views.course_front_api import CourseFilterView, CourseListPagination, CourseDetailView, \
    EpisodeDetailView
from frontend_api.views.single_page_api import RulePageView, AboutUsPageView, PrivacyPageView, FaqPageView, \
    HelpPageView, BugPageView, CriticismPageView, SuggestionPageView, ComplaintPageView, StaticFormRegisterView
from frontend_api.views.consult_front_api import ConsultSearchView

urlpatterns = [
    # blog
    path('Content/BlogList/', BlogSearchView.as_view(), name='blog_search_view'),
    path('Content/BlogListPagination/', BlogListPagination.as_view(), name='blog_list_pagination_view'),
    path('Content/BlogDetail/', BlogDetailView.as_view(), name='blog_view'),
    path('Content/BlogFilters/', BlogFilterView.as_view(), name='blog_filters'),
    # service
    path('Content/ServiceDetail/', ServiceDetailView.as_view(), name='service_view'),
    path('Content/ServiceList/', ServiceSearchView.as_view(), name='service_view'),
    # base page
    path('Content/BasePageDetail/', BasePageDetailView.as_view(), name='base_page_view'),
    # post
    path('Content/PostDetail/', PostDetailView.as_view(), name='post_view'),
    path('Content/PostList/', PostSearchView.as_view(), name='post_search_view'),
    
    # story
    path('Content/StoryList/', StoryListView.as_view(), name='story_view'),
    # work sample
    path('Content/WorkSampleList/', WorkSampleSearchView.as_view(), name='work_sample_search_view'),
    path('Content/WorkSampleDetail/', WorkSampleDetailView.as_view(), name='work_sample_view'),

    # about us
    path('Content/AboutUsDetail/', AboutUsDetailView.as_view(), name='about_us_view'),

    # why us
    path('Content/WhyUsDetail/', WhyUsDetailView.as_view(), name='why_us_view'),
    path('Content/WhyUsList/', WhyUsSearchView.as_view(), name='why_us_search_view'),

    # course
    path('Content/CourseFilters/', CourseFilterView.as_view(), name='course_filters'),
    path('Content/CourseListPagination/', CourseListPagination.as_view(), name='course_list_pagination'),
    path('Content/CourseDetail/', CourseDetailView.as_view(), name='episode_detail'),

    # episode
    path('Content/EpisodeDetail/', EpisodeDetailView.as_view(), name='epsiode_detail'),

    # single_page
    path('SinglePage/ContactUs/', ContactInfoView.as_view(), name='contact_single_page'),
    path('SinglePage/Rule/', RulePageView.as_view(), name='rule_single_page'),
    path('SinglePage/Privacy/', PrivacyPageView.as_view(), name='privacy_single_page'),
    path('SinglePage/AboutUs/', AboutUsPageView.as_view(), name='about_us_single_page'),
    path('SinglePage/Faq/', FaqPageView.as_view(), name='faq_single_page'),
    path('SinglePage/Help/', HelpPageView.as_view(), name='help_single_page'),
    path('SinglePage/Bug/', BugPageView.as_view(), name='bug_single_page'),
    path('SinglePage/Criticism/', CriticismPageView.as_view(), name='criticism_single_page'),
    path('SinglePage/Suggestion/', SuggestionPageView.as_view(), name='suggestion_single_page'),
    path('SinglePage/Complaint/', ComplaintPageView.as_view(), name='complaint_single_page'),
    path('SinglePage/StaticFormRegister/', StaticFormRegisterView.as_view(), name='static_form_single_page'),

    # index
    path('Site/Index/', IndexAPIView.as_view(), name='index_api'),

    # consult
    path('Front/ConsultByUrl/', ConsultSearchView.as_view(), name="consults_by_url"),

    # task_manager
    path('Content/TaskRequestDetail/', TaskRequestDetailView.as_view(), name="get_task_req")
]
