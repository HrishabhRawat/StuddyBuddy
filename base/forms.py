from django.forms import ModelForm
from .models import Room, User 
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room     # specify the model that we want to create a form for
        fields = '__all__'   # it will create the form based on the metadata of this Room 
        exclude = ['host', 'participants']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
