import { useState, useEffect } from 'react';
import { useTasks } from '../hooks/useTasks';
import { TaskForm } from '../components/TaskForm';
import { TaskTable } from '../components/TaskTable';
import '../App.css';

function App() {
  // State to manage filter status
  const [filter, setFilter] = useState(() => {
    return localStorage.getItem("taskFilter") ?? "All";
  });

  // Extracting tasks and logic from our custom hook
  const { 
    tasks, 
    addTask, 
    updateTaskStatus, 
    deleteTask, 
    editTask, 
    sortTasksByDeadline 
  } = useTasks();

  // useEffect hook to save filter state to local storage whenever it changes
  useEffect(() => {
    localStorage.setItem("taskFilter", filter);
  }, [filter]);

  return (
    <>
      <h1>Welcome to the To Do App</h1>
      <p>Manage your tasks efficiently!</p>
      
      <div className="log-out-container">
        <button className='log-out-btn' onClick={() => {
          localStorage.removeItem('token');
          window.location.href = '/'; // Redirect to login page
        }}>Log out</button>
      </div>
      
      {/* Component handling form inputs and task creation */}
      <TaskForm addTask={addTask} />

      <div className='filter-container'>
        <button className='filter-button' onClick={
          () => {
            const statusList = ["All", "Done", "Undone"];
            const nextIndex = (statusList.indexOf(filter) + 1) % statusList.length;
            setFilter(statusList[nextIndex]);
          }
        }> Filter By status</button>Current filter: {filter}
        
        <button className='sort-button' onClick={sortTasksByDeadline}>
          Sort by Deadline
        </button>
      </div>

      {/* Component displaying the list of tasks and handling edits/deletions */}
      <TaskTable 
        tasks={tasks} 
        filter={filter} 
        updateTaskStatus={updateTaskStatus} 
        deleteTask={deleteTask} 
        editTask={editTask} 
      />
    </>
  );
}

export default App;