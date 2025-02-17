from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# 09388783263

class Course(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive')
    ]
    DISCOUNT_TYPE_CHOICES = [
        (1, 'Static'),
        (2, 'Percent')
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
                              related_name='course_photo')
    video = models.ForeignKey('file_manager.FileManager', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='course_video')
    category = models.ForeignKey('course.CourseCategory', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='course_category')
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='course_content')
    count_share = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_view = models.IntegerField(default=0)
    count_sale = models.IntegerField(default=0)
    count_session = models.IntegerField(null=True, blank=True)
    hours = models.BigIntegerField(null=True, blank=True)
    progress = models.IntegerField(
        validators=[
            MinValueValidator(0),  # Ensures progress is not less than 0
            MaxValueValidator(100)  # Ensures progress is not more than 100
        ]
    )
    rate = models.FloatField(default=0)
    abstract = models.TextField(max_length=3000, null=True, blank=True)
    description = models.TextField(max_length=3000, null=True, blank=True)
    features = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    price = models.BigIntegerField(null=True, blank=True)
    is_discount = models.BooleanField(default=False)
    discount = models.BigIntegerField(null=True, blank=True)
    discount_type = models.PositiveIntegerField(choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True)
    discount_end = models.DateTimeField(blank=True, null=True)
    is_discount_time = models.BooleanField(default=False)
    consultant = models.ForeignKey('security.User', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="course_consult")
    writer = models.ForeignKey('security.User', blank=True, null=True, on_delete=models.SET_NULL,
                               related_name="course_writer")
    has_installment = models.BooleanField(default=False)
    installment_count = models.PositiveIntegerField(null=True, blank=True)
    question_value = models.JSONField(default=list)
    student_count = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)
    create_row_date = models.DateTimeField(auto_now_add=True)
    update_row_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'course_course'
