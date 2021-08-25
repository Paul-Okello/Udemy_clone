from django.db import models
import uuid


# Sector model
class Sector(models.Model):
    name = models.CharField(max_length=255)
    sector_uuid = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4,
                                   editable=False,
                                   unique=True)
    related_courses = models.ManyToManyField('Course',
                                             related_name='related_courses')
    sector_image = models.ImageField(upload_to='sector_image',
                                     blank=True,
                                     null=True)


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
    course_section = models.ManyToManyField('CourseSection')
    comments = models.ManyToManyField('Comment', blank=True)
    image_url = models.ImageField(upload_to='course_images', blank=True)
    course_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title


# CourseSection models
class CourseSection(models.Model):
    section_title = models.CharField(max_length=255)
    episodes = models.ManyToManyField('Episode')
    created_at = models.DateTimeField(auto_now_add=True)


# Episode models
class Episode(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_episodes')
    length = models.DecimalField(decimal_places=2, max_digits=10)


# Comment models
class Comment(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)