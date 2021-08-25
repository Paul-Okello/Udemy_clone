from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course
from users.serializers import UserSerializer


class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_students')
    author = UserSerializer()
    image_url = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = Course
        fields = [
            'course_uuid', 'title', 'description', 'student_no', 'author',
            'price', 'image_url'
        ]