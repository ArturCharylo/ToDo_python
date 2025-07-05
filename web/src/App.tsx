import React, {useState, useEffect} from 'react'
import axios from 'axios'
import './App.css'

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

  // Fetch tasks from the API when the component mounts
  // This function retrieves the tasks from the backend and updates the state
  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/")
      setTasks(response.data)
    }
    catch (error){
      console.error("Error fetching tasks:", error)
    }
  }

  // useEffect hook runs on app startup to fetch tasks
  // This ensures that the task list is populated when the app loads
  useEffect(() => {
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
    // Filter tasks based on the current filter state
    const filteredTasks = filter === "All"
      ? tasks
      : tasks.filter(task => task.completed === filter)

    return(
      <table className='task-table'>
        <thead className='task-table-header'>
          <tr>
            <th>Numer zadania</th>
            <th>Tytuł</th>
            <th>Opis</th>
            <th>Status</th>
            <th>Deadline</th>
            <th>Update Status</th>
            <th>Delete Task</th>
          </tr>
        </thead>
        <tbody className='task-table-body'>
          {filteredTasks.map((task) => (
            <tr key={task.task_number}>
              <td>{task.task_number}</td>
              <td>{task.title}</td>
              <td>{task.description}</td>
              <td>{task.completed}</td>
              <td>{new Date(task.deadline).toLocaleDateString()}</td>
              <td><button onClick={(e) => {
                e.preventDefault()
                UpdateTask(task)
                // Update the task status locally independently of the API response
                // This is to ensure the UI reflects the change immediately
                setTasks(tasks.map(t => 
                  t.task_number === task.task_number 
                    ? { ...t, completed: t.completed === "Done" ? "Undone" : "Done" } 
                    : t
                ));

              }}>Update Status</button></td>
              <td><button onClick={(e) => {
                e.preventDefault()
                DeleteTask(task)
              }}>Delete Task</button></td>
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
      await axios.delete(`http://localhost:8000/api/delete/${task.task_number}/`)
      setTasks(tasks.filter(t => t.task_number !== task.task_number))
    }
    catch (error) {
      console.error("Error deleting task:", error)
    }
  }

  return (
    <>
      <h1>Welcome to the To Do App</h1>
      <p>Manage your tasks efficiently!</p>
      <form onSubmit={handleSubmit} className='task-form'>
        <input type="text" placeholder="Add a title for a new task" value={title} onChange={(e) => {
          setTitle(e.target.value)
        }}/>
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
