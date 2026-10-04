from django.db import models
from django.contrib.auth.models import User


def profile_photo_path(instance, filename):
	return f'profile_photos/{instance.user_id}/{filename}'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone_number = models.CharField(max_length=30, blank=True)
	bio = models.CharField(max_length=240, blank=True)
	photo = models.ImageField(upload_to=profile_photo_path, blank=True)

	def __str__(self):
		return f'{self.user.username} profile'
