from django.db import models

from cms.models import Survey
from security.models import User


class UserSurvey(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # bigInt NOT NULL
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    answer = models.CharField(max_length=3000, null=True, blank=True)  # nvarchar(3000) NULL
    create_row_date = models.DateTimeField(auto_now_add=True)  # datetime2(7) NOT NULL
    update_row_date = models.DateTimeField(auto_now=True)  # datetime2(7) NOT NULL
    is_deleted = models.BooleanField(default=False)  # bit NOT NULL
    status = models.IntegerField()  # int NOT NULL

    class Meta:
        db_table = 'activity_user_survey'
        verbose_name_plural = 'User Surveys'

    def __str__(self):
        return f'User Survey {self.id}'
