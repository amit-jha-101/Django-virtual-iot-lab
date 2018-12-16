from django import forms
from .models import Device,Rule


class DeviceCreationForm(forms.ModelForm):
  class Meta:
    model = Device
    fields = ['name','desc','api']


class RuleCreationForm(forms.ModelForm):
  class Meta:
    model = Rule
    fields = '__all__'
