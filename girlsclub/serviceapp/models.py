from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    price_for_new = models.IntegerField()
    price_for_old = models.IntegerField()
    event_photo_id = models.CharField(max_length=50)
    ticket_photo_id = models.CharField(max_length=50)
    description = models.TextField()
    event_date = models.DateField(null=True)


class MemberGirl(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    unique_id = models.CharField(max_length=50)
    discussion_topics = models.TextField()
    joining_purpose = models.TextField()


class Newsletter(models.Model):
    photo_id = models.CharField(max_length=50)
    text = models.TextField()
