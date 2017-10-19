from django import forms
from captcha.fields import ReCaptchaField
# from home.models import Registration
# from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios, FieldWithButtons, StrictButton


class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)



class AllauthSignupForm(forms.Form):
 
     captcha = ReCaptchaField()
 
     def __init__(self, *args, **kwargs):
         super(AllauthSignupForm, self).__init__(*args, **kwargs)
 
         field_order = ['username', 'email', 'password1', 'password2', 'captcha']
         self.order_fields(field_order)
 
     def signup(self, request, user):
         """ Required, or else it throws deprecation warnings """
         pass







