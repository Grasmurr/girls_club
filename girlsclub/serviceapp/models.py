from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price_for_new = models.IntegerField()
    price_for_old = models.IntegerField()
    event_photo_id = models.CharField(max_length=100)
    ticket_photo_id = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateField(null=True, max_length=100)


class MemberGirl(models.Model):
    telegram_id = models.BigIntegerField(null=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    unique_id = models.CharField(max_length=50)
    discussion_topics = models.TextField()
    joining_purpose = models.TextField()
    old_or_new = models.TextField(null="new")


class Newsletter(models.Model):
    number = models.IntegerField(null=True)
    photo_id = models.TextField()
    text = models.TextField()


class UnregisteredGirl(models.Model):
    telegram_id = models.BigIntegerField(null=True)
    is_registered = models.BooleanField(default=False)

