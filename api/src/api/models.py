from django.db import models

# Model representing a single ToDo task in the database
class Task(models.Model):
    task_number = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.CharField(max_length=20, default='Undone')

    def __str__(self):
        return f"{self.task_number}: {self.title}"