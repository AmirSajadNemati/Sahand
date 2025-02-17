from rest_framework import serializers

from course.models import CourseUser
from payment.models import Transaction


class BuyCourseRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    is_full = serializers.BooleanField()

class BuyCourseResponseSerializer(serializers.Serializer):
    pay_id = serializers.IntegerField()
    status = serializers.CharField()
    pay_url = serializers.CharField()


class TransactionSerializer(serializers.ModelSerializer):
    course_title = serializers.SerializerMethodField()
    course_photo = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_course_title(self, obj):
        course_user = CourseUser.objects.filter(transactions__contains=[obj.id]).first()
        return course_user.course.title if course_user else None

    def get_course_photo(self, obj):
        course_user = CourseUser.objects.filter(transactions__contains=[obj.id]).first()
        return course_user.course.photo.id if course_user.course.photo else None