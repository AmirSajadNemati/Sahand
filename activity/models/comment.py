from django.db import models
from security.models import User

class Comment(models.Model):

    OBJECT_TYPE_CHOICES = [
        (1, 'Course'),
        (2, 'Blog'),
        (3, 'WorkSample'),
        (4, 'Post'),
        (5, 'Story'),
        (6, 'Service')
    ]

    COMMENT_TYPE_CHOICES = [
        (1, 'نظر'),
        (2, 'امتیاز'),
        (3, 'هردو')
    ]
    object_type = models.IntegerField(choices=OBJECT_TYPE_CHOICES)  # Equivalent to int NOT NULL
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Foreign key to User model
    related_id = models.BigIntegerField()  # Represents RelatedId
    comment_date = models.DateTimeField(auto_now=True)  # Equivalent to datetime2(7) NOT NULL
    comment_type = models.IntegerField(choices=COMMENT_TYPE_CHOICES)  # Equivalent to int NOT NULL
    rate = models.IntegerField(default=0)  # Equivalent to int NOT NULL
    comment_text = models.TextField(null=True, blank=True)  # nvarchar(250) NULL
    comment_answer = models.TextField(null=True, blank=True)  # nvarchar(250) NULL
    positives = models.BigIntegerField(default=0, null=True, blank=True)  # Storing positive score as an integer
    negatives = models.BigIntegerField(default=0, null=True, blank=True)  # Storing negative score as an integer
    create_row_date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    update_row_date = models.DateTimeField(auto_now=True)  # Automatically updated on save
    is_deleted = models.BooleanField(default=False)  # Equivalent to bit NOT NULL
    status = models.IntegerField(default=0)  # Equivalent to int NOT NULL

    class Meta:
        db_table = 'activity_comment'  # Specify the database table name
        verbose_name_plural = 'Comments'  # Optional: For admin display

    def __str__(self):
        return f'Comment {self.id} by User {self.user_id}'
