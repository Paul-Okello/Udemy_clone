from django.db import models
from django.contrib.auth import get_user_model
import uuid
from decimal import Decimal
from .helpers import get_timer
from mutagen.mp4 import MP4, MP4StreamInfoError


# Sector model
class Sector(models.Model):
    name = models.CharField(max_length=255)
    sector_uuid = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4,
                                   editable=False,
                                   unique=True)
    related_courses = models.ManyToManyField('Course',
                                             related_name='related_courses',
                                             blank=True)
    sector_image = models.ImageField(upload_to='sector_image',
                                     blank=True,
                                     null=True)

    def get_image_absolute_url(self):
        return "http://localhost:8000" + self.sector_image.url


# Create your models here.
class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("users.User",
                               on_delete=models.CASCADE,
                               related_name="author")
    language = models.CharField(max_length=50)
    course_section = models.ManyToManyField('CourseSection', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    image_url = models.ImageField(upload_to='course_images', blank=True)
    course_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    def get_brief_description(self):
        return self.description[:100]

    def get_enrolled_students(self):
        students = get_user_model().objects.filter(paid_courses=self)
        return len(students)

    def get_total_classes(self):
        classes = 0
        for section in self.course_section:
            classes += len(section.episodes.all())
        return classes

    def total_course_lengths(self):
        lengths = Decimal(0.0)
        for section in self.course_section:
            for episode in section.episodes.all():
                lengths += episode.length

        return get_timer(lengths, type="short")

    def get_image_absolute_url(self):
        return "http://localhost:8000" + self.image_url.url


# CourseSection models
class CourseSection(models.Model):
    section_title = models.CharField(max_length=255)
    episodes = models.ManyToManyField('Episode', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_length(self):
        total = Decimal(0.0)
        for episode in self.episodes.all():
            total += episode.length
        return get_timer(total, type="min")


# Episode models
class Episode(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_episodes')
    length = models.DecimalField(decimal_places=2, max_digits=10)

    def get_video_length(self):
        try:
            video = MP4(self.file)
            return video.info.length
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def get_absolute_url(self):
        return "http://localhost:8000" + self.file.url

    def save(self, *args, **kwargs):
        self.length = self.get_video_length()
        return super().save(*args, **kwargs)


# Comment models
class Comment(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)