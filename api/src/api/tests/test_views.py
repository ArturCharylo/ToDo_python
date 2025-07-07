from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Task


class TaskApiTests(APITestCase):

    def setUp(self):
        # Create a test task
        self.task = Task.objects.create(
            task_number=1,
            title='Test Task',
            completed=False
        )

    def test_get_task_list(self):
        url = reverse('api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_add_task(self):
        url = reverse('task_add')
        data = {'title': 'Nowe zadanie'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.latest('id').title, 'Nowe zadanie')

    def test_update_task_status(self):
        url = reverse('task_status_update', args=[self.task.task_number])
        data = {'completed': 'Done'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, 'Done')

    def test_delete_task(self):
        url = reverse('delete_task', args=[self.task.task_number])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(
            task_number=self.task.task_number).exists())
