import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth endpoints
export const authAPI = {
  register: async (email, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, { email, password })
    return response.data
  },
  login: async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },
  getMe: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

// Sweets endpoints
export const sweetsAPI = {
  getAll: async () => {
    const response = await api.get('/sweets')
    return response.data
  },
  search: async (params) => {
    const response = await api.get('/sweets/search', { params })
    return response.data
  },
  create: async (sweetData) => {
    const response = await api.post('/sweets', sweetData)
    return response.data
  },
  update: async (id, sweetData) => {
    const response = await api.put(`/sweets/${id}`, sweetData)
    return response.data
  },
  delete: async (id) => {
    await api.delete(`/sweets/${id}`)
  },
  purchase: async (id) => {
    const response = await api.post(`/sweets/${id}/purchase`)
    return response.data
  },
  restock: async (id, quantity) => {
    const response = await api.post(`/sweets/${id}/restock`, { quantity })
    return response.data
  },
}

export default api
