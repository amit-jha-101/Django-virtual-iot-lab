from django.db import models
from django.utils import timezone

# from django.contrib.auth.models import User


class Device(models.Model):
  id=models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  desc = models.TextField()
  date_created= models.DateTimeField(default=timezone.now)
  api=models.TextField()
  
  # author = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.name

class Rule(models.Model):
  id = models.AutoField(primary_key=True)
  name=models.CharField(max_length=100)
  ruleDescription =  models.TextField(blank=True, null=True)
  sensor=models.ForeignKey(Device,on_delete=models.CASCADE)
  RULE_TYPES=(
    ('lb','LOWER_BOUND'),
    ('ub', 'UPPER_BOUND'),
    ('eq', 'EQUALITY'),
  )
  Rule_type=models.CharField(max_length=2,choices=RULE_TYPES)
  ruleValue=models.IntegerField()
  rule_field=models.CharField(max_length=100)
  ruleFlag = models.BooleanField(default=True)


class Type(models.Model):
  """
    This model will be used to store the thing types in the database
    and later the information of the type will be used while creating a thing 
    and attaching a type to it

    @thingTypeName: stores the name of the thing type
    @thingTypeProperties:The ThingTypeProperties for the thing type to create.
     It contains information about the new thing type including a description, and a list of searchable thing attribute names.

      thingTypeDescription:The description of the thing type.
      searchableAttributes: A list of searchable thing attribute names.
    @tags:Metadata which can be used to manage the thing type.
      A set of key/value pairs that are used to manage the resource.
        Key --
        The tag's key.
        Value  --
        The tag's value.


  """
  thingTypeName = models.CharField(primary_key = True, max_length = 100)
  thingTypeProperties = models.TextField(blank=True, null=True)
  tags = models.TextField(blank = True, null = True)

  def __str__(self):
    return "ThingTypeName : "+self.thingTypeName 