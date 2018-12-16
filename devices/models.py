from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User


class Device(models.Model):
  name = models.CharField(max_length=100)
  desc = models.TextField()
  date_created= models.DateTimeField(default=timezone.now)
  api=models.TextField()
  
  # author = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.name

class Rule(models.Model):
  name=models.CharField(max_length=100)
  sensor=models.ForeignKey(Device,on_delete=models.CASCADE)
  RULE_TYPES=(
    ('lb','LOWER_BOUND'),
    ('ub', 'UPPER_BOUND'),
    ('eq', 'EQUALITY'),
  )
  Rule_type=models.CharField(max_length=2,choices=RULE_TYPES)
  ruleValue=models.IntegerField()
  rule_field=models.CharField(max_length=100)
  

