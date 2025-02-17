from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Episode(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    title = models.CharField(max_length=250, null=True, blank=True)
    english_title = models.CharField(max_length=250, null=True, blank=True, unique=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[^_]*$',
                                             message="Underscores are not allowed in the title."
                                         )
                                     ]
                                     )
    photo = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='episode_photo')
    file = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='episode_file')
    description = models.TextField(max_length=1000, null=True, blank=True)
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='episode_content')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='episode_course')
    video_link = models.CharField(max_length=2500, null=True, blank=True)
    parent = models.ForeignKey('course.Episode', blank=True, on_delete=models.SET_NULL, null=True,
                               related_name='episode_parent')
    is_video = models.BooleanField()
    is_test = models.BooleanField()
    is_project = models.BooleanField()
    is_free = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'course_episode'
