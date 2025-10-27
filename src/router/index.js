import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MajorInfo from '../views/MajorInfo.vue'
import Login from '../views/Login.vue'
import Upload from '../views/Upload.vue'
import Register from '../views/Register.vue'  // 引入 Register.vue
import Profile from '../views/Profile.vue' // 引入 Profile.vue

const routes = [
  { path: '/', component: Home },
  { path: '/major/:name', component: MajorInfo },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile }, // 添加 Profile 路由
  { path: '/upload', component: Upload },
  { path: '/register', component: Register }  // 添加注册路由
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
