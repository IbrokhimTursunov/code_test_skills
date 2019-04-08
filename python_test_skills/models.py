from django.db import models
from django.contrib.auth.models import User

class PythonTasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    initial_code = models.TextField(default='')
    right_code = models.TextField(default='')

class PythonTestResults(models.Model):
    test_id = models.ForeignKey(PythonTasks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_code = models.TextField(default='')
    user_result = models.BooleanField(default='')
