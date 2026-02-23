import React, { useState } from 'react';
import type { Task } from '../hooks/useTasks';

type TaskTableProps = {
  tasks: Task[];
  filter: string;
  updateTaskStatus: (task: Task) => Promise<void>;
  deleteTask: (task: Task) => Promise<void>;
  editTask: (taskNumber: number, updatedData: Partial<Task>) => Promise<void>;
};

export const TaskTable: React.FC<TaskTableProps> = ({ 
  tasks, 
  filter, 
  updateTaskStatus, 
  deleteTask, 
  editTask 
}) => {
  // Local state to track which task is currently being edited
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Displays all the tasks that have been fetched from the API in the table on the web
  const filteredTasks = filter === "All"
    ? tasks
    : tasks.filter(task => task.completed === filter);

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
  };

  const handleEditSave = async () => {
    if (editingTask) {
      await editTask(editingTask.task_number, {
        title: editingTask.title,
        description: editingTask.description,
        deadline: editingTask.deadline,
      });
      setEditingTask(null);
    }
  };

  return (
    <table className='task-table'>
      <thead className='task-table-header'>
        <tr>
          <th>Task Number</th>
          <th>Title</th>
          <th>Description</th>
          <th>Status</th>
          <th>Deadline</th>
          <th>Update Status</th>
          <th>Delete Task</th>
          <th>Edit Task</th>
        </tr>
      </thead>
      <tbody className='task-table-body'>
        {filteredTasks.map((task) => (
          <tr key={task.task_number}>
            <td>{task.task_number}</td>
            {editingTask?.task_number === task.task_number ? (
              <>
                <td>
                  <input
                    type="text"
                    className="edit-input"
                    value={editingTask.title}
                    onChange={e => setEditingTask({...editingTask, title: e.target.value})}
                  />
                </td>
                <td>
                  <input
                    type="text"
                    className="edit-input"
                    value={editingTask.description}
                    onChange={e => setEditingTask({...editingTask, description: e.target.value})}
                  />
                </td>
                <td>{editingTask.completed}</td>
                <td>
                  <input
                    type="date"
                    className="edit-input"
                    value={editingTask.deadline}
                    onChange={e => setEditingTask({...editingTask, deadline: e.target.value})}
                  />
                </td>
                <td>
                  <button disabled>Update Status</button>
                </td>
                <td>
                  <button disabled>Delete Task</button>
                </td>
                <td>
                  <button onClick={handleEditSave}>Save</button>
                  <button onClick={() => setEditingTask(null)}>Cancel</button>
                </td>
              </>
            ) : (
              <>
                <td>{task.title}</td>
                <td>{task.description}</td>
                <td>{task.completed}</td>
                <td>{new Date(task.deadline).toLocaleDateString()}</td>
                <td>
                  <button onClick={(e) => {
                    e.preventDefault();
                    updateTaskStatus(task);
                  }}>Update Status</button>
                </td>
                <td>
                  <button onClick={(e) => {
                    e.preventDefault();
                    deleteTask(task);
                  }}>Delete Task</button>
                </td>
                <td>
                  <button onClick={(e) => {
                    e.preventDefault();
                    handleEditClick(task);
                  }}>Edit Task</button>
                </td>
              </>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  );
};