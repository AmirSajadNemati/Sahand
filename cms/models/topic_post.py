from django.db import models

from security.models import User


class TopicPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='author_name')
    topic = models.ForeignKey('cms.Topic', on_delete=models.SET_NULL, null=True, blank=True, related_name='topic')
    post_date = models.DateTimeField()
    text = models.TextField(max_length=3000, null=True, blank=True)
    replay = models.ForeignKey('cms.TopicPost', on_delete=models.SET_NULL, null=True, blank=True, related_name='topic_post_reply')
    is_verified = models.BooleanField()
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'cms_topic_post'
