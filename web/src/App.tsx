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

function App() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [deadline, setDeadline] = useState("")
  const [tasks, setTasks] = useState<Task[]>([])

  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/")
      setTasks(response.data)
    }
    catch (error){
      console.error("Error fetching tasks:", error)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!title || !description || !deadline) {
      alert("Please fill in all fields")
      return
    }
  const newTask: Task = {
      task_number: tasks.length + 1,
      title,
      description,
      deadline,
      timestamp: new Date().toISOString(),
      completed: "Undone"
    }

    AddTask(newTask)
    setTasks([...tasks, newTask])
    setTitle("")
    setDescription("")
    setDeadline("")
  }

  const displayTasks = () => {
    return(
      <table>
        <thead>
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
        <tbody>
          {tasks.map((task) => (
            <tr key={task.task_number}>
              <td>{task.task_number}</td>
              <td>{task.title}</td>
              <td>{task.description}</td>
              <td>{task.completed}</td>
              <td>{new Date(task.deadline).toLocaleDateString()}</td>
              <td><button>Update Status</button></td>
              <td><button>Delete Task</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    )
  }

  const AddTask = async (task: Task) => {
    try {
      await axios.post("http://localhost:8000/api/add/", task)
    }
    catch (error) {
      console.error("Error adding task:", error)
    }
  }

  return (
    <>
      <div>To Do App</div>
      <div className="App">
        <h1>Welcome to the To Do App</h1>
        <p>Manage your tasks efficiently!</p>
        <form onSubmit={handleSubmit}>
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
        {displayTasks()}
      </div>
    </>
  )
}

export default App
