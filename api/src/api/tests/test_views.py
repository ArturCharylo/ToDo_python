from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Task


class TaskApiTests(APITestCase):

    def setUp(self):
        # Create a test task
        # Using 'Undone' since completed is now a CharField
        self.task = Task.objects.create(
            title='Test Task',
            completed='Undone'
        )

    def test_get_task_list(self):
        # In DRF routers, the list view is named '<basename>-list'
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_add_task(self):
        # POST requests also go to the '-list' URL
        url = reverse('task-list')
        data = {'title': 'Nowe zadanie'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        # The primary key is 'task_number' now, not 'id'
        self.assertEqual(Task.objects.latest('task_number').title, 'Nowe zadanie')

    def test_update_task_status(self):
        # Detail views in DRF routers are named '<basename>-detail'
        url = reverse('task-detail', args=[self.task.task_number])
        data = {'completed': 'Done'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, 'Done')

    def test_delete_task(self):
        # DELETE requests go to the '-detail' URL
        url = reverse('task-detail', args=[self.task.task_number])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(
            task_number=self.task.task_number).exists())