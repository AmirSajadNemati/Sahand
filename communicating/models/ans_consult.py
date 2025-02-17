from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class AnswerConsult(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    file = models.ForeignKey('file_manager.FileManager', on_delete=models.CASCADE, null=True, blank=True,
                             related_name='answer_consult_file')
    form_fields = models.JSONField(default=dict)
    form_answers = models.JSONField(default=dict)
    req_consult = models.ForeignKey('communicating.RequestConsult', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="answer_consult_req")
    consult = models.ForeignKey('communicating.Consult', on_delete=models.CASCADE, null=True, blank=True,
                                related_name="answer_consult_consult")

    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'communicating_answer_consult'
