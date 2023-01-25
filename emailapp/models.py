from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# inbuild model-django User
# user model provides:
# username,first_name,last_name,email,password


# user defined model


class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)







