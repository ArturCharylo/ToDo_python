from django.test import TestCase
from api.models import Task


class TaskModelTests(TestCase):

    def test_task_number_auto_increment(self):
        task1 = Task.objects.create(title='Pierwsze')
        task2 = Task.objects.create(title='Drugie')
        self.assertEqual(task2.task_number, task1.task_number + 1)

    def test_default_completed_value(self):
        task = Task.objects.create(title='Test domyślnej wartości')
        self.assertEqual(task.completed, 'Undone')

    def test_str_method(self):
        task = Task.objects.create(title='Tytuł zadania')
        # Updated to match the new __str__ format: f"{self.task_number}: {self.title}"
        self.assertEqual(str(task), f"{task.task_number}: Tytuł zadania")