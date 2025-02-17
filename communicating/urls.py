from django.urls import path
from communicating.views import (ConsultAddOrUpdateView, ConsultGetListView, ConsultGetView, ConsultDeleteView,
                                 ConsultUndeleteView,
                                 AnswerConsultAddOrUpdateView, AnswerConsultGetListView, AnswerConsultGetView,
                                 AnswerConsultDeleteView,
                                 AnswerConsultUndeleteView, RequestConsultAddOrUpdateView, RequestConsultGetListView,
                                 RequestConsultGetView, RequestConsultDeleteView, RequestConsultUndeleteView, )

urlpatterns = [
    # consult
    path('ConsultAddOrUpdate/', ConsultAddOrUpdateView.as_view(), name="consult_add_or_update"),
    path('ConsultList/', ConsultGetListView.as_view(), name="consult_get_list"),
    path('ConsultGet/', ConsultGetView.as_view(), name="consult_get"),
    path('ConsultDelete/', ConsultDeleteView.as_view(), name="consult_delete"),
    path('ConsultUnDelete/', ConsultUndeleteView.as_view(), name="consult_undelete"),

    # answer_consult
    path('AnswerConsultAddOrUpdate/', AnswerConsultAddOrUpdateView.as_view(), name="answer_consult_add_or_update"),
    path('AnswerConsultList/', AnswerConsultGetListView.as_view(), name="answer_consult_get_list"),
    path('AnswerConsultGet/', AnswerConsultGetView.as_view(), name="answer_consult_get"),
    path('AnswerConsultDelete/', AnswerConsultDeleteView.as_view(), name="answer_consult_delete"),
    path('AnswerConsultUnDelete/', AnswerConsultUndeleteView.as_view(), name="answer_consult_undelete"),

    # req_consult
    path('RequestConsultAddOrUpdate/', RequestConsultAddOrUpdateView.as_view(), name="req_consult_add_or_update"),
    path('RequestConsultList/', RequestConsultGetListView.as_view(), name="req_consult_get_list"),
    path('RequestConsultGet/', RequestConsultGetView.as_view(), name="req_consult_get"),
    path('RequestConsultDelete/', RequestConsultDeleteView.as_view(), name="req_consult_delete"),
    path('RequestConsultUnDelete/', RequestConsultUndeleteView.as_view(), name="req_consult_undelete"),

]
