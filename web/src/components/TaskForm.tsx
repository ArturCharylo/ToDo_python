import React, { useState } from 'react';
import type { NewTask } from '../hooks/useTasks';

type TaskFormProps = {
  addTask: (task: NewTask) => Promise<void>;
};

export const TaskForm: React.FC<TaskFormProps> = ({ addTask }) => {
  // State for handling form inputs
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [deadline, setDeadline] = useState("");

  // Function that handles code behaviour after user submits the form for adding tasks
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title || !description || !deadline) {
      alert("Please fill in all fields");
      return;
    }

    const newTask: NewTask = {
      title,
      description,
      deadline,
      timestamp: new Date().toISOString(),
      completed: "Undone"
    };

    await addTask(newTask);
    
    // Clear the form after successful submission
    setTitle("");
    setDescription("");
    setDeadline("");
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        placeholder="Add a title for a new task"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input 
        type="text" 
        placeholder="Add a description for the new task" 
        value={description} 
        onChange={(e) => setDescription(e.target.value)}
      />
      <input 
        type="date" 
        placeholder="Select a due date" 
        value={deadline} 
        onChange={(e) => setDeadline(e.target.value)}
      />
      <button type="submit">Add Task</button>
    </form>
  );
};