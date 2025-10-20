import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://192.168.187.135:5000', // 后端 Flask 或 FastAPI 服务地址
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    console.error('❌ 请求出错:', error)
    return Promise.reject(error)
  }
)

export default request
