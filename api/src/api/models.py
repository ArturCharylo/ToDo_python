from django.db import models

# Create your models here.


class Task(models.Model):
    task_number = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.TextField(blank=True, default='Undone')

    def save(self, *args, **kwargs):
        if self.task_number is None:
            last_task = Task.objects.order_by('-task_number').first()
            if last_task and last_task.task_number:
                self.task_number = last_task.task_number + 1
            else:
                self.task_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-id']  # Order by ID descending
