from django import forms
from .models import AppUser, Interest, Interest2,KeyVal
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class AppUserForm(forms.ModelForm):

    class Meta():
        model = AppUser
        fields = ('user_id', 'profile_pic', 'locale', 'birthyear',
                  'gender', 'location', 'timezone')


class KeyValForm(forms.ModelForm):
    class Meta():
        model=KeyVal
        fields=('container','interest_level')


# class Interest2Form(forms.ModelForm):
#     # bf = forms.BooleanField()

#     # def __init__(self, *args, **kwargs):
#     # self.fields['in']
#     interest_name = forms.ModelMultipleChoiceField(label="Add New interests",
#                                                    widget=forms.CheckboxSelectMultiple,
#                                                    queryset=Interest.objects.all())
#     # self.fields['del_member'] = forms.ModelMultipleChoiceField(label="Remove interest",
#     #                                                            widget=forms.CheckboxSelectMultiple,
#     #                                                            queryset=Interest.objects.filter(pk__in=self.project.members.all()))

#     interest_level = forms.DecimalField(
#         decimal_places=1, max_digits=6,
#     )

#     class Meta():
#         model = Interest2
#         fields = ('interest_name', 'interest_level')
