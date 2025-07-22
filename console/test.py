import unittest
from unittest.mock import patch, MagicMock
import ToDo


class TestTaskManager(unittest.TestCase):
    @patch('ToDo.requests.get')
    def test_load_tasks_success(self, mock_get):
        # preapare
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'task_number': 1, 'title': 'Test'}]
        mock_get.return_value = mock_response

        # execute
        tasks = ToDo.load_tasks()

        # assert
        self.assertEqual(tasks, [{'task_number': 1, 'title': 'Test'}])
        mock_get.assert_called_once_with(ToDo.API_URL)

    @patch('ToDo.requests.get')
    def test_load_tasks_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        tasks = ToDo.load_tasks()

        self.assertEqual(tasks, [])

    @patch('ToDo.requests.post')
    def test_add_task_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        with patch('builtins.print') as mock_print:
            ToDo.add_task('Tytuł', 'Opis', '2025-07-07')

            mock_post.assert_called_once()
            mock_print.assert_any_call("Zadanie 'Tytuł' zostało dodane.")

    @patch('ToDo.load_tasks')
    def test_display_tasks_all(self, mock_load_tasks):
        mock_load_tasks.return_value = [{
            'task_number': 1,
            'title': 'Test',
            'description': 'Opis',
            'deadline': '2025-07-07',
            'timestamp': '2025-07-06T12:00:00',
            'completed': 'Done'
        }]

        ToDo.task_filter = 'wszystkie'
        with patch('builtins.print') as mock_print:
            ToDo.display_tasks()
            # Test if the task is printed correctly
            printed = [call.args[0] for call in mock_print.call_args_list]
            self.assertTrue(any('numer: 1' in line for line in printed))

    @patch('ToDo.requests.patch')
    def test_mark_task_as_done_success(self, mock_patch):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_patch.return_value = mock_response

        with patch('builtins.print') as mock_print:
            ToDo.mark_task_as_done(1)
            mock_patch.assert_called_once()
            mock_print.assert_any_call(
                "Zadanie o numerze 1 zostało oznaczone jako wykonane.")

    @patch('ToDo.requests.delete')
    def test_delete_task_success(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        with patch('builtins.print') as mock_print:
            ToDo.delete_task(1)
            mock_delete.assert_called_once()
            mock_print.assert_any_call("Zadanie o numerze 1 zostało usunięte.")

    @patch('builtins.input', side_effect=['2'])
    @patch('ToDo.display_tasks')
    def test_display_menu_option_2(self, mock_display_tasks, mock_input):
        ToDo.display_menu()
        mock_display_tasks.assert_called_once()


if __name__ == '__main__':
    unittest.main()
