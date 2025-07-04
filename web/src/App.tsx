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
    
    setTasks([
      ...tasks,
      {
        task_number: tasks.length + 1,
        title,
        description,
        deadline,
        timestamp: new Date().toISOString(),
        completed: "Undone"
      }
    ])
    setTitle("")
    setDescription("")
    setDeadline("")
  }

  const displayTasks = () => {
    return tasks.map((task, index) => (
      <div key={index} className="task">
        <p>
          Numer zadania: {task.task_number} Tytuł: {task.title} - Opis: {task.description} Status: {task.completed} Deadline: {task.deadline}
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
