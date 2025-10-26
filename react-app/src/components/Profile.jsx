import { useState, useEffect } from 'react'
import './Profile.css'

function Profile({ isLoggedIn }) {
  const [userInfo, setUserInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (isLoggedIn) {
      fetchUserInfo()
    }
  }, [isLoggedIn])

  const fetchUserInfo = async () => {
    setIsLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        setError('请先登录')
        setIsLoading(false)
        return
      }

      const response = await fetch('http://localhost:8000/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.error) {
          setError(data.error)
        } else {
          setUserInfo(data)
        }
      } else {
        setError('获取用户信息失败')
      }
    } catch (error) {
      setError('网络错误: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setUserInfo(null)
    setError('已退出登录')
    // 可以添加重定向逻辑或调用父组件的登出回调
  }

  if (isLoading) {
    return <div className="profile-container">加载中...</div>
  }

  return (
    <div className="profile-container">
      <h2>用户信息</h2>
      {error && <p className="error">{error}</p>}
      {userInfo && (
        <div className="user-info">
          <p><strong>用户ID:</strong> {userInfo.user_id}</p>
          <p><strong>用户名:</strong> {userInfo.username}</p>
          <button onClick={handleLogout} className="logout-button">
            退出登录
          </button>
        </div>
      )}
    </div>
  )
}

export default Profile