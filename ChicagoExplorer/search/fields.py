from django import forms
from django.shortcuts import render
from django.http import HttpResponse



class IntegerRange(forms.MultiValueField):
  def __init__(self, *args, **kwargs):
      fields = (forms.IntegerField(),
                forms.IntegerField())
      super(IntegerRange, self).__init__(fields=fields,
                                         *args, **kwargs)
  def compress(self,values):
      if values and (values[0] is None or values[1] is None):
          raise forms.ValidationError('Must fill in both min and max price')
      return values

class PriceRange(IntegerRange):
  def compress(self,values):
      super(PriceRange, self).compress(values)
      for v in values:
          if not (1 <= v <= 1000000):
              raise forms.ValidationError('Price bounds must be in range 1 to 1000000')
      if values and (values[1] < values[0]):
          raise forms.ValidationError('Min price must not exceed max price')
      return values




  
