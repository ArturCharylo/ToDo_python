import '@testing-library/jest-dom';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './pages/App';
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock window.alert and window.location to prevent JSDom errors during testing
beforeAll(() => {
  window.alert = vi.fn();
  Object.defineProperty(window, 'location', {
    value: { href: '/' },
    writable: true,
  });
});

// Set a fake token before each test so the app doesn't try to log out the test environment
beforeEach(() => {
  localStorage.setItem('token', 'fake-test-token');
  localStorage.setItem('taskFilter', 'All');
  vi.clearAllMocks();
});

test('renders header and form inputs', async () => {
  render(<App />);
  expect(screen.getByText(/Welcome to the To Do App/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Add a title/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Add a description/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/Select a due date/i)).toBeInTheDocument();
});

test('fetches and displays tasks on mount', async () => {
  mockedAxios.get.mockResolvedValueOnce({
    data: [
      {
        task_number: 1,
        title: 'Test Task',
        description: 'Some desc',
        deadline: new Date().toISOString(),
        timestamp: new Date().toISOString(),
        completed: 'Undone'
      }
    ]
  });

  render(<App />);
  
  expect(await screen.findByText('Test Task')).toBeInTheDocument();
});

test('can add a new task', async () => {
  mockedAxios.get.mockResolvedValueOnce({ data: [] }); // No tasks initially
  mockedAxios.post.mockResolvedValueOnce({});
  mockedAxios.get.mockResolvedValueOnce({
    data: [
      {
        task_number: 2,
        title: 'New Task',
        description: 'Desc',
        deadline: new Date().toISOString(),
        timestamp: new Date().toISOString(),
        completed: 'Undone'
      }
    ]
  });

  render(<App />);
  
  fireEvent.change(screen.getByPlaceholderText(/Add a title/i), { target: { value: 'New Task' } });
  fireEvent.change(screen.getByPlaceholderText(/Add a description/i), { target: { value: 'Desc' } });
  fireEvent.change(screen.getByPlaceholderText(/Select a due date/i), { target: { value: '2025-07-07' } });
  fireEvent.click(screen.getByText(/Add Task/i));

  expect(await screen.findByText('New Task')).toBeInTheDocument();
});

test('can filter tasks by status', async () => {
  mockedAxios.get.mockResolvedValueOnce({
    data: [
      { task_number: 1, title: 'Done Task', description: '', deadline: '', timestamp: '', completed: 'Done' },
      { task_number: 2, title: 'Undone Task', description: '', deadline: '', timestamp: '', completed: 'Undone' }
    ]
  });

  render(<App />);
  expect(await screen.findByText('Done Task')).toBeInTheDocument();
  expect(screen.getByText('Undone Task')).toBeInTheDocument();

  fireEvent.click(screen.getByText(/Filter By status/i));

  await waitFor(() => {
    expect(screen.queryByText('Undone Task')).not.toBeInTheDocument();
    expect(screen.getByText('Done Task')).toBeInTheDocument();
  });
});

describe('App', () => {
  it('updates task status when clicking "Update Status"', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: [
        {
          task_number: 1,
          title: 'Test Task',
          description: '',
          deadline: new Date().toISOString(),
          timestamp: '',
          completed: 'Undone'
        }
      ]
    });

    mockedAxios.patch.mockResolvedValueOnce({});

    render(<App />);

    expect(await screen.findByText('Test Task')).toBeInTheDocument();

    const updateButtons = screen.getAllByRole('button', { name: /Update Status/i });
    fireEvent.click(updateButtons[0]);

    await waitFor(() => {
      expect(mockedAxios.patch).toHaveBeenCalledWith(
        'http://localhost:8000/api/update/1/',
        { completed: 'Done' }
      );
    });
  });

  it('deletes a task when clicking "Delete Task"', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: [
        {
          task_number: 1,
          title: 'Test Task',
          description: '',
          deadline: new Date().toISOString(),
          timestamp: '',
          completed: 'Undone'
        }
      ]
    });

    mockedAxios.delete.mockResolvedValueOnce({});

    render(<App />);

    expect(await screen.findByText('Test Task')).toBeInTheDocument();

    const deleteButtons = screen.getAllByRole('button', { name: /Delete Task/i });
    fireEvent.click(deleteButtons[0]);

    await waitFor(() => {
      expect(mockedAxios.delete).toHaveBeenCalledWith(
        'http://localhost:8000/api/delete/1/'
      );
    });
  });
});