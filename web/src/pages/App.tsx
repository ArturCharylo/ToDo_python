import React, {useState, useEffect} from 'react'
import axios from 'axios'
import '../App.css'

type Task = {
  task_number: number
  title: string
  description: string
  deadline: string
  timestamp: string
  completed: string
  // id is present in API but not used in UI
}

type NewTask = Omit<Task, "task_number">


function App() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [deadline, setDeadline] = useState("")
  const [filter, setFilter] = useState(() => {
    return localStorage.getItem("taskFilter") ?? "All";
  }) // State to manage filter status
  const [tasks, setTasks] = useState<Task[]>([])
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Fetch tasks from the API when the component mounts
  // This function retrieves the tasks from the backend and updates the state
  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/")
      setTasks(response?.data ?? [])
    }
    catch (error){
      console.error("Error fetching tasks:", error)
    }
  }

  // useEffect hook runs on app startup to fetch tasks
  // This ensures that the task list is populated when the app loads
  useEffect(() => {
    if (!localStorage.getItem('token')) {
      alert("You are not logged in. Please log in to continue.");
      window.location.href = '/'; // Redirect to login if no token is found
    }
    fetchTasks()
  }, [])

  useEffect(() => {
    localStorage.setItem("taskFilter", filter);
  }, [filter]);

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  if (!title || !description || !deadline) {
    alert("Please fill in all fields")
    return
  }

  const newTask: NewTask = {
    title,
    description,
    deadline,
    timestamp: new Date().toISOString(),
    completed: "Undone"
  }

  await AddTask(newTask)
  await fetchTasks()  
  setTitle("")
  setDescription("")
  setDeadline("")
}

  const displayTasks = () => {
    const filteredTasks = filter === "All"
      ? tasks
      : tasks.filter(task => task.completed === filter)

    return(
      <table className='task-table'>
        <thead className='task-table-header'>
          <tr>
            <th>Task Number</th>
            <th>Tile</th>
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
                      e.preventDefault()
                      UpdateTask(task)
                      setTasks(tasks.map(t => 
                        t.task_number === task.task_number 
                          ? { ...t, completed: t.completed === "Done" ? "Undone" : "Done" } 
                          : t
                      ));
                    }}>Update Status</button>
                  </td>
                  <td>
                    <button onClick={(e) => {
                      e.preventDefault()
                      DeleteTask(task)
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
    )
  }

  const AddTask = async (task: NewTask) => {
    try {
      await axios.post("http://localhost:8000/api/add/", task)
    }
    catch (error) {
      console.error("Error adding task:", error)
    }
  }

  const UpdateTask = async (task: Task) => {
    try {
      await axios.patch(`http://localhost:8000/api/update/${task.task_number}/`, {
        completed: task.completed === "Done" ? "Undone" : "Done"
      })
    }
    catch (error) {
      console.error("Error updating task:", error)
    }
  }

  const DeleteTask = async (task: Task) => {
    try {
      await axios.delete(`http://localhost:8000/api/delete/${task.task_number}/`,{
      })
      setTasks(tasks.filter(t => t.task_number !== task.task_number))
    }
    catch (error) {
      console.error("Error deleting task:", error)
    }
  }

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
  };

  const handleEditSave = async () => {
    if (editingTask) {
      try {
        await axios.patch(`http://localhost:8000/api/update/${editingTask.task_number}/`, {
          title: editingTask.title,
          description: editingTask.description,
          deadline: editingTask.deadline,
        });
        await fetchTasks();
        setEditingTask(null);
      } catch (error) {
        console.error("Error saving edited task:", error);
      }
    }
  };

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
      <form onSubmit={handleSubmit} className='task-form'>
        <input
          type="text"
          placeholder="Add a title for a new task"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value)
          }}
        />
        <input type="text" placeholder="Add a description for the new task" value={description} onChange={(e) => {
          setDescription(e.target.value)
        }}/>
        <input type="date" placeholder="Select a due date" value={deadline} onChange={(e) => {
          setDeadline(e.target.value)
        }}/>
        <button type="submit">Add Task</button>
      </form>
      <div className='filter-container'>
        <button className='filter-button' onClick={
          () => {
            const statusList = ["All", "Done", "Undone"];
            const nextIndex = (statusList.indexOf(filter) + 1) % statusList.length;
            setFilter(statusList[nextIndex]);
          }
        }> Filter By status</button>Current filter: {filter}
        <button className='sort-button' onClick={() => {
          tasks.sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
          setTasks([...tasks]); // Trigger re-render by updating state
        }}>Sort by Deadline</button>
      </div>
      {displayTasks()}
    </>
  )
}

export default App
