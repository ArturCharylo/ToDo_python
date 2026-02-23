import { useState, useEffect } from 'react';
import axios from 'axios';

// Exporting types so they can be reused in other components
export type Task = {
  task_number: number;
  title: string;
  description: string;
  deadline: string;
  timestamp: string;
  completed: string;
};

export type NewTask = Omit<Task, "task_number">;

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);

  // Fetch tasks from the API when the component mounts
  // This function retrieves the tasks from the backend and updates the state
  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/tasks/");
      setTasks(response?.data ?? []);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // useEffect hook runs on app startup to fetch tasks
  // This ensures that the task list is populated when the app loads
  useEffect(() => {
    if (!localStorage.getItem('token')) {
      alert("You are not logged in. Please log in to continue.");
      window.location.href = '/'; // Redirect to login if no token is found
    }
    fetchTasks();
  }, []);

  // Handles adding a task via an API request
  const addTask = async (task: NewTask) => {
    try {
      await axios.post("http://localhost:8000/api/tasks/", task);
      await fetchTasks();
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  // Handles changing task status in the database via an API request („Done” ⇄ „Undone”)
  const updateTaskStatus = async (task: Task) => {
    try {
      const newStatus = task.completed === "Done" ? "Undone" : "Done";
      await axios.patch(`http://localhost:8000/api/tasks/${task.task_number}/`, {
        completed: newStatus
      });
      // Update local state to avoid an extra API call
      setTasks(tasks.map(t =>
        t.task_number === task.task_number
          ? { ...t, completed: newStatus }
          : t
      ));
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  // Handles deleting tasks from the database via an API request
  const deleteTask = async (task: Task) => {
    try {
      await axios.delete(`http://localhost:8000/api/tasks/${task.task_number}/`);
      setTasks(tasks.filter(t => t.task_number !== task.task_number));
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  // Handles saving edited task data
  const editTask = async (taskNumber: number, updatedData: Partial<Task>) => {
    try {
      await axios.patch(`http://localhost:8000/api/tasks/${taskNumber}/`, updatedData);
      await fetchTasks();
    } catch (error) {
      console.error("Error saving edited task:", error);
    }
  };

  // Helper function to sort tasks locally
  const sortTasksByDeadline = () => {
    const sorted = [...tasks].sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
    setTasks(sorted);
  };

  return { 
    tasks, 
    addTask, 
    updateTaskStatus, 
    deleteTask, 
    editTask, 
    sortTasksByDeadline 
  };
};