import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
})

export function setAuthToken(token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const savedToken = localStorage.getItem('token')
if (savedToken) setAuthToken(savedToken)

export default api
