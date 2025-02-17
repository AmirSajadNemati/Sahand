from django.urls import path

from info.views import ColleagueAddOrUpdateView, ColleagueGetListView, ColleagueGetView, ColleagueDeleteView, \
    ColleagueUndeleteView, CustomerCommentAddOrUpdateView, CustomerCommentGetListView, CustomerCommentGetView, \
    CustomerCommentDeleteView, CustomerCommentUndeleteView, HonorAddOrUpdateView, HonorGetListView, HonorGetView, \
    HonorDeleteView, HonorUndeleteView, SiteFeatureAddOrUpdateView, SiteFeatureGetListView, SiteFeatureGetView, \
    SiteFeatureDeleteView, SiteFeatureUndeleteView, StatisticAddOrUpdateView, StatisticGetListView, StatisticGetView, \
    StatisticDeleteView, StatisticUndeleteView, TeamAddOrUpdateView, TeamGetListView, TeamGetView, TeamDeleteView, \
    TeamUndeleteView, TimeLineAddOrUpdateView, TimeLineGetListView, TimeLineGetView, TimeLineDeleteView, \
    TimeLineUndeleteView, WhyUsAddOrUpdateView, WhyUsGetListView, WhyUsGetView, WhyUsDeleteView, WhyUsUndeleteView

urlpatterns = [
    # Colleague
    path('ColleagueAddOrUpdate/', ColleagueAddOrUpdateView.as_view(), name="colleague_add_or_update"),
    path('ColleagueList/', ColleagueGetListView.as_view(), name="colleague_get_list"),
    path('ColleagueGet/', ColleagueGetView.as_view(), name="colleague_get"),
    path('ColleagueDelete/', ColleagueDeleteView.as_view(), name="colleague_delete"),
    path('ColleagueUnDelete/', ColleagueUndeleteView.as_view(), name="colleague_undelete"),

    # CustomerComment
    path('CustomerCommentAddOrUpdate/', CustomerCommentAddOrUpdateView.as_view(),
         name="customer_comment_add_or_update"),
    path('CustomerCommentList/', CustomerCommentGetListView.as_view(), name="customer_comment_get_list"),
    path('CustomerCommentGet/', CustomerCommentGetView.as_view(), name="customer_comment_get"),
    path('CustomerCommentDelete/', CustomerCommentDeleteView.as_view(), name="customer_comment_delete"),
    path('CustomerCommentUnDelete/', CustomerCommentUndeleteView.as_view(), name="customer_comment_undelete"),

    # Honor
    path('HonorAddOrUpdate/', HonorAddOrUpdateView.as_view(), name="honor_add_or_update"),
    path('HonorList/', HonorGetListView.as_view(), name="honor_get_list"),
    path('HonorGet/', HonorGetView.as_view(), name="honor_get"),
    path('HonorDelete/', HonorDeleteView.as_view(), name="honor_delete"),
    path('HonorUnDelete/', HonorUndeleteView.as_view(), name="honor_undelete"),

    # SiteFeature
    path('SiteFeatureAddOrUpdate/', SiteFeatureAddOrUpdateView.as_view(), name="site_feature_add_or_update"),
    path('SiteFeatureList/', SiteFeatureGetListView.as_view(), name="site_feature_get_list"),
    path('SiteFeatureGet/', SiteFeatureGetView.as_view(), name="site_feature_get"),
    path('SiteFeatureDelete/', SiteFeatureDeleteView.as_view(), name="site_feature_delete"),
    path('SiteFeatureUnDelete/', SiteFeatureUndeleteView.as_view(), name="site_feature_undelete"),

    # Statistic
    path('StatisticAddOrUpdate/', StatisticAddOrUpdateView.as_view(), name="statistic_add_or_update"),
    path('StatisticList/', StatisticGetListView.as_view(), name="statistic_get_list"),
    path('StatisticGet/', StatisticGetView.as_view(), name="statistic_get"),
    path('StatisticDelete/', StatisticDeleteView.as_view(), name="statistic_delete"),
    path('StatisticUnDelete/', StatisticUndeleteView.as_view(), name="statistic_undelete"),

    # Team
    path('TeamAddOrUpdate/', TeamAddOrUpdateView.as_view(), name="team_add_or_update"),
    path('TeamList/', TeamGetListView.as_view(), name="team_get_list"),
    path('TeamGet/', TeamGetView.as_view(), name="team_get"),
    path('TeamDelete/', TeamDeleteView.as_view(), name="team_delete"),
    path('TeamUnDelete/', TeamUndeleteView.as_view(), name="team_undelete"),

    # TimeLine
    path('TimeLineAddOrUpdate/', TimeLineAddOrUpdateView.as_view(), name="time_line_add_or_update"),
    path('TimeLineList/', TimeLineGetListView.as_view(), name="time_line_get_list"),
    path('TimeLineGet/', TimeLineGetView.as_view(), name="time_line_get"),
    path('TimeLineDelete/', TimeLineDeleteView.as_view(), name="time_line_delete"),
    path('TimeLineUnDelete/', TimeLineUndeleteView.as_view(), name="time_line_undelete"),

    # WhyUs
    path('WhyUsAddOrUpdate/', WhyUsAddOrUpdateView.as_view(), name="why_us_add_or_update"),
    path('WhyUsList/', WhyUsGetListView.as_view(), name="why_us_get_list"),
    path('WhyUsGet/', WhyUsGetView.as_view(), name="why_us_get"),
    path('WhyUsDelete/', WhyUsDeleteView.as_view(), name="why_us_delete"),
    path('WhyUsUnDelete/', WhyUsUndeleteView.as_view(), name="why_us_undelete"),
]
