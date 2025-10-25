import { useState } from 'react'
import Login from './components/Login'
import Profile from './components/Profile'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  const handleLoginSuccess = () => {
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>FastAPI + React 应用</h1>
        <div className="auth-status">
          {isLoggedIn ? (
            <div>
              <span className="status-text">已登录</span>
              <button onClick={handleLogout} className="logout-button">
                退出登录
              </button>
            </div>
          ) : (
            <span className="status-text">未登录</span>
          )}
        </div>
      </header>

      <main className="app-main">
        {!isLoggedIn ? (
          <Login onLoginSuccess={handleLoginSuccess} />
        ) : (
          <Profile isLoggedIn={isLoggedIn} />
        )}
      </main>

      <footer className="app-footer">
        <p>Cookie 认证示例 - FastAPI 后端 + React 前端</p>
      </footer>
    </div>
  )
}

export default App
