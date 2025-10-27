import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://192.168.187.135:5000', // Flask 后端地址
  timeout: 5000,
  withCredentials: false
})

// ✅ 请求拦截器：添加 JWT token，并区分上传文件和普通请求
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}` // 自动携带登录 token
  }

  // 🚀 如果是 FormData，不设置 Content-Type（浏览器自动带 boundary）
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type']
  } else {
    config.headers['Content-Type'] = 'application/json'
  }

  return config
})

// ✅ 响应拦截器：统一错误处理
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      console.error(`❌ 请求错误: ${error.response.status}`, error.response.data)
      if (error.response.status === 401) {
        alert('登录已过期，请重新登录')
        localStorage.removeItem('token')
        location.href = '/login'
      }
    } else {
      console.error('❌ 网络错误或服务器无响应:', error)
    }
    return Promise.reject(error)
  }
)

export default request
