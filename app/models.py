from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import CustomUser



class Category(models.Model):
	name = models.CharField("カテゴリ", max_length=50)

	def __str__(self):
		return self.name

class Price(models.Model):
	price = models.CharField("プライス", max_length=50)

	def __str__(self):
		return self.price

class Score(models.Model):
	scores = models.CharField("おすすめ度", max_length=50)

	def __str__(self):
		return self.scores
