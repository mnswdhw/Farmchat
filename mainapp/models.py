import email

from djongo import models

# Create your models here.


class Review(models.Model):
    rating = models.PositiveIntegerField(blank=True, null=True)
    user_review = models.TextField()
    objects = models.DjongoManager()


class Expert(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.BigIntegerField()
    qualification = models.CharField(max_length=255)
    objects = models.DjongoManager()


class Reference(models.Model):
    disease = models.TextField()
    image_url = models.TextField()
    objects = models.DjongoManager()


class ImgData(models.Model):
    s3link = models.TextField()
    captions_user = models.TextField()
    audio_text = models.TextField()
    objects = models.DjongoManager()
