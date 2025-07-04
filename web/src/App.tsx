import React, {useState} from 'react'
import './App.css'

function App() {
const [title, setTitle] = useState("")
const [description, setDescription] = useState("")
const [dueDate, setDueDate] = useState("")
const [tasks, setTasks] = useState<string[]>([])

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault()
  if (!title || !description || !dueDate) {
    alert("Please fill in all fields")
    return
  }
  else{
    setTasks([...tasks, `${title} - ${description} (Due: ${dueDate})`])
    displayTasks()
  }
}

const displayTasks = () => {
  return tasks.map((task, index) => (
    <div key={index} className="task">
      <p>{task}</p>
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
      </div>
    </>
  )
}

export default App
