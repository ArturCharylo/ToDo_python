# tests/test_main_window.py

from unittest.mock import patch, AsyncMock
import pytest
from ui.main_window import MainWindow


@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_initial_state(main_window):
    assert main_window.windowTitle() == "ToDo App - Desktop"
    assert main_window.task_filter == "wszystkie"
    assert main_window.task_title.placeholderText() == "Wpisz tytuł nowego zadania"
    assert main_window.task_list.count() == 0


def test_add_task_to_listwidget(main_window):
    task = {'task_number': 1, 'title': 'Test Task', 'deadline': '2025-07-10'}
    main_window.add_task_to_listwidget(task, '✅', 'dzisiaj')
    assert main_window.task_list.count() == 1
    text = main_window.task_list.item(0).text()
    assert "Test Task" in text
    assert "✅" in text
    assert "(do: 2025-07-10)" in text


@pytest.mark.asyncio
async def test_add_task_success(main_window, qtbot):
    # Ustawiamy pola tekstowe
    main_window.task_title.setText("Nowe zadanie")
    main_window.task_description.setText("Opis")
    main_window.task_deadline.setText("2025-07-10")

    # Mockujemy metody i API
    with patch('ui.main_window.add_task_to_api', new_callable=AsyncMock) as mock_api, \
            patch('ui.main_window.QMessageBox.information') as mock_info, \
            patch('ui.main_window.QMessageBox.warning'), \
            patch.object(main_window, 'load_tasks', new_callable=AsyncMock):

        mock_response = AsyncMock()
        mock_response.status = 201
        mock_api.return_value = mock_response

        # Uruchamiamy metodę
        await main_window._add_task_async("Nowe zadanie", "Opis", "2025-07-10")

        # Sprawdzenia
        mock_info.assert_called_once()
        assert main_window.task_title.text() == ""
        assert main_window.task_description.text() == ""
        assert main_window.task_deadline.text() == ""


def test_change_filter(main_window):
    main_window.change_filter("wykonane")
    assert main_window.task_filter == "wykonane"


def test_delete_selected_task(main_window, qtbot):
    task = {'task_number': 1, 'title': 'Test', 'deadline': '2025-07-10'}
    main_window.add_task_to_listwidget(task, '✅', 'dzisiaj')
    item = main_window.task_list.item(0)
    item.setSelected(True)

    with patch('ui.main_window.asyncio.ensure_future') as mock_ensure:
        main_window.delete_selected_task()
        mock_ensure.assert_called_once()
