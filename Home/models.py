from django.db import models

# Create your models here.
class Message(models.Model):
    body = models.CharField(max_length=100)
    time = models.DateTimeField(default=None, null=True)
    uid = models.CharField(max_length=100)
    
    def __str__(self):
        return self.body