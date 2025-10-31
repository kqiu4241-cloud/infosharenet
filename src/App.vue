<template>
  <div id="app">
    <header class="header">
      <h1>🎓 23级信息工程学院资料网</h1>
      <nav>
        <router-link to="/">首页</router-link> |
        <router-link to="/login">登录</router-link> |
        <router-link to="/upload">上传资料</router-link>
      </nav>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLoggedIn = ref(false)
const router = useRouter()

// 页面加载时检查登录状态
onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    // 已登录
    isLoggedIn.value = true
  }
})

// 退出登录的操作
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  router.push('/login')
}
</script>


<style>
body {
  margin: 0;
  font-family: "Microsoft YaHei", sans-serif;
  background: #f8f9fa;
}
.header {
  text-align: center;
  padding: 20px;
  background: #0059b3;
  color: white;
}
.header a {
  color: #fff;
  margin: 0 10px;
  text-decoration: none;
}
.main {
  padding: 20px;
}
</style>
