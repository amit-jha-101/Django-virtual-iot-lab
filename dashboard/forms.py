from django import forms
import boto3
client = boto3.client('iot')
res = client.list_thing_types()
let = res.get('thingTypes')
l = []
for i in let:
    x = (i.get('thingTypeName'),i.get('thingTypeName'))
    l.append(x)

class ThingCreate(forms.Form):
    Thing_Name = forms.CharField(max_length=100)
    Thing_Description = forms.CharField(widget=forms.Textarea(attrs={'width':"100%",'cols':""}))
    Thing_Type = forms.CharField(label="Enter thing Type",widget=forms.Select(choices=l))
    
