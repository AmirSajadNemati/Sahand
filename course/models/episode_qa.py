from django.db import models


class EpisodeQA(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    content = models.ForeignKey('content_manager.ContentManager', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='ep_qa_question')
    user = models.ForeignKey('security.User', null=True, blank=True, on_delete=models.CASCADE,
                             related_name='ep_qa_user')
    author = models.ForeignKey('security.User', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='ep_qa_author')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='ep_qa_parent')
    course = models.ForeignKey('course.Course', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='ep_qa_course')
    episode = models.ForeignKey('course.Episode', null=True, blank=True, on_delete=models.CASCADE,
                                related_name='ep_qa_episode')
    file = models.ForeignKey('file_manager.FileManager', null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='ep_qa_file')
    is_author = models.BooleanField(default=False)
    count_share = models.IntegerField(default=0)
    count_reply = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'course_episode_qa'