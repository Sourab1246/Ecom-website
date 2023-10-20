from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']

        def clean(self):
            cleaned_data=super().clean()
            password1=cleaned_data.get('password1')
            password2=cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('password doesnot match')

            return cleaned_data     

class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ShippingAddressForm(forms.Form):
    shipping_address=forms.CharField(label='shipping_address',max_length=200,required=True)
    city = forms.CharField(label='City', max_length=100, required=True)
    state = forms.CharField(label='State', max_length=100, required=True)
    zip_code = forms.CharField(label='ZIP Code', max_length=10, required=True)
    country = forms.CharField(label='Country', max_length=100, required=True)
    phone_number = forms.CharField(label='Phone Number', max_length=20, required=True)
   
class OrderForm(forms.Form):
    product=forms.CharField()
    quantity=forms.IntegerField()
    payment_option=forms.CharField(max_length=20)

class ProductSearchForm(forms.Form):
    search_query=forms.CharField(max_length=100,required=False,label='Search')    