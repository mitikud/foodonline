from django import forms

from accounts.validator import allow_only_image_validator
from .models import User, UserProfile

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username','email', 'phone_number', 'password']

#         def clean(self):
#             cleaned_data = super(UserForm, self).clean()
#             password = cleaned_data.get('password')
#             confirm_password = cleaned_data.get('confirm_password')
#             print(password, confirm_password)
#             if password != confirm_password:
#                 raise forms.ValidationError("password does not match")


#for registration purposes only
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        # print(password)
        # print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )    

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typying ...','required':'required'}))
    # profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_image_validator])
    # cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_image_validator])
    # make latitude and longitude readeonly ===method 1
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model= UserProfile
        # we don't need this line we are getting from google
        # fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state','city', 'pin_code', 'latitude', 'longitude']
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state','city', 'pin_code', 'latitude', 'longitude']
    # make latitude and longitude readeonly ===method 2
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readeonly']='readeonly'


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']