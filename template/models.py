from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("user", "title")
