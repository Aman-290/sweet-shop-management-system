import { createContext, useState, useContext, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in and fetch user data
    const token = localStorage.getItem('token')
    if (token) {
      fetchUserData()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUserData = async () => {
    try {
      const userData = await authAPI.getMe()
      setUser(userData)
    } catch (error) {
      // Token invalid or expired, clear it
      localStorage.removeItem('token')
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const register = async (email, password) => {
    try {
      await authAPI.register(email, password)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }

  const login = async (email, password) => {
    try {
      const data = await authAPI.login(email, password)
      localStorage.setItem('token', data.access_token)
      
      // Fetch user data including role
      const userData = await authAPI.getMe()
      setUser(userData)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  const value = {
    user,
    loading,
    register,
    login,
    logout,
    isAdmin: user?.role === 'admin',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
