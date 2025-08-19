from django.contrib.auth.forms import UserCreationForm

from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 
            'password1', 
            'password2', 
            'lastname', 
            'firstname', 
            'middlename', 
            "address", 
            "telephone", 
            "function",
            "role",
            "department",
            # "subregion",
            # "provinces"
        )