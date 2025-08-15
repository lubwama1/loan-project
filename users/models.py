from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Gender(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHERS = 'Others', 'Others'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(
        blank=True, upload_to='profile_pics', default='default.jpg')
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.OTHERS)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img_path = self.image.path
        img = Image.open(img_path)
        max_size = (500, 500)
        if img.height > 500 or img.width > 500:
            img.thumbnail(max_size)
            img.save(img_path)