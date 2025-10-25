import { useState, useEffect } from 'react'
import './Profile.css'

function Profile({ isLoggedIn }) {
  const [userInfo, setUserInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchProfile = async () => {
    if (!isLoggedIn) return
    
    setIsLoading(true)
    setError('')
    
    try {
      const response = await fetch('http://localhost:8000/profile', {
        method: 'GET',
        credentials: 'include', // 重要：包含cookies
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        setUserInfo(data)
      } else {
        setError('获取用户信息失败')
      }
    } catch (error) {
      setError('网络错误: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchProfile()
  }, [isLoggedIn])

  if (!isLoggedIn) {
    return (
      <div className="profile-container">
        <p className="not-logged-in">请先登录查看用户信息</p>
      </div>
    )
  }

  return (
    <div className="profile-container">
      <h2>用户信息</h2>
      
      {isLoading && <p className="loading">加载中...</p>}
      
      {error && <p className="error">{error}</p>}
      
      {userInfo && (
        <div className="user-info">
          <div className="info-item">
            <strong>用户ID:</strong> 
            <span>{userInfo.user_id || '未获取到用户ID'}</span>
          </div>
          <button onClick={fetchProfile} className="refresh-button">
            刷新信息
          </button>
        </div>
      )}
    </div>
  )
}

export default Profile