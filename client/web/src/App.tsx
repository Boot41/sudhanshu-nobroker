import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Sample from './pages/Sample'
import Home from './pages/Home'

function App() {
  const [count, setCount] = useState(0)

  if (typeof window !== 'undefined' && window.location) {
    const path = window.location.pathname
    if (path === '/home') return <Home />
    if (path === '/sample') return <Sample />
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <p style={{ marginBottom: 12 }}>
        <a href="/home" style={{ marginRight: 16 }}>Open Home page →</a>
        <a href="/sample">Open UI Atoms Sample page →</a>
      </p>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
