import '@testing-library/jest-dom';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;


test('renders header and form inputs', () => {
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
  
  // Wait for the task to be displayed
  expect(await screen.findByText('Test Task')).toBeInTheDocument();
});


test('can add a new task', async () => {
  mockedAxios.get.mockResolvedValueOnce({ data: [] }); // No tasks initially
  mockedAxios.post.mockResolvedValueOnce({});
  mockedAxios.get.mockResolvedValueOnce({ // Get tasks again after adding
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

  // After adding, the new task should be displayed
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

  // Click the filter button
  fireEvent.click(screen.getByText(/Filter By status/i));

  // Only the 'Done' tasks should be displayed"
  await waitFor(() => {
    expect(screen.queryByText('Undone Task')).not.toBeInTheDocument();
    expect(screen.getByText('Done Task')).toBeInTheDocument();
  });
});
