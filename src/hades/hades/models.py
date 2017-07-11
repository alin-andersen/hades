import uuid

from django.db import models

class Page(models.Model):
	uuid  = models.UUIDField(default=uuid.uuid4,editable=False)
	order = models.PositiveIntegerField('Order',default=2,blank=False,null=False)
	span  = models.PositiveIntegerField('Timespan (in seconds)',default=10,blank=False,null=False)