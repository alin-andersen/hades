import uuid

from django.db import models

class Setting(models.Model):
	uuid  = models.UUIDField(default=uuid.uuid4,editable=False)
	animation_in = models.CharField(max_length=128)
	timespan_in  = models.PositiveIntegerField(default=0)
	animation_out = models.CharField(max_length=128)
	timespan_out = models.PositiveIntegerField(default=0)
	background_color = models.CharField(max_length=128)

class Page(models.Model):
	uuid  = models.UUIDField(default=uuid.uuid4,editable=False)
	order = models.PositiveIntegerField('Order',default=2,blank=False,null=False)
	span  = models.PositiveIntegerField('Timespan (in seconds)',default=10,blank=False,null=False)