import React, {useState, useEffect} from 'react'
import axios from 'axios'
import './App.css'

type Task = {
  title: string
  description: string
  dueDate: string
  status: string
}

function App() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [dueDate, setDueDate] = useState("")
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
    if (!title || !description || !dueDate) {
      alert("Please fill in all fields")
      return
    }
    setTasks([
      ...tasks,
      {
        title,
        description,
        dueDate,
        status: "niewykonane"
      }
    ])
    setTitle("")
    setDescription("")
    setDueDate("")
  }

  const displayTasks = () => {
    return tasks.map((task, index) => (
      <div key={index} className="task">
        <p>
          Tytuł: {task.title} - Opis: {task.description} Status: {task.status} Deadline: {task.dueDate}
        </p>
      </div>
    ))
  }

  return (
    <>
      <div>To Do App</div>
      <div className="App">
        <h1>Welcome to the To Do App</h1>
        <p>Manage your tasks efficiently!</p>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Add a title for a new task" onChange={(e) => {
            setTitle(e.target.value)
          }}/>
          <input type="text" placeholder="Add a description for the new task" onChange={(e) => {
            setDescription(e.target.value)
          }}/>
          <input type="date" placeholder="Select a due date" onChange={(e) => {
            setDueDate(e.target.value)
          }}/>
          <button type="submit">Add Task</button>
        </form>
        {displayTasks()}
      </div>
    </>
  )
}

export default App
