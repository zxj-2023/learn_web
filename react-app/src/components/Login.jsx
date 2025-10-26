import { useState } from 'react'
import './Login.css'

function Login({ onLoginSuccess }) {
    const [isLoading, setIsLoading] = useState(false)
    const [message, setMessage] = useState('')

    const handleLogin = async () => {
        setIsLoading(true)
        setMessage('')

        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            if (response.ok) {
                const data = await response.json()
                // 将JWT token存储到localStorage
                localStorage.setItem('access_token', data.access_token)
                setMessage(data.msg)
                onLoginSuccess()
            } else {
                setMessage('登录失败')
            }
        } catch (error) {
            setMessage('网络错误: ' + error.message)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="login-container">
            <h2>用户登录</h2>
            <button
                onClick={handleLogin}
                disabled={isLoading}
                className="login-button"
            >
                {isLoading ? '登录中...' : '登录'}
            </button>
            {message && <p className="message">{message}</p>}
        </div>
    )
}

export default Login