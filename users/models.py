from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Counter(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    onBreak = models.BooleanField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.count)