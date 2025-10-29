<template>
  <div class="login">
    <h2>🔑 登录</h2>
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" type="password" placeholder="密码" />
    <button @click="login">登录</button>
    <p>还没有账号？<router-link to="/register">注册</router-link></p> <!-- 跳转到注册页面 -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../api/request'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

// 登录成功后，存储用户数据
const login = async () => {
  const res = await request.post('/auth/login', {
    username: username.value,
    password: password.value
  })
  console.log(res)
  if (res.token) {
    // 存储 token 和 user 数据
    localStorage.setItem('token', res.token)
    localStorage.setItem('user', JSON.stringify({
      username: res.username,
      avatar: res.avatar || '默认头像链接'  // 如果没有 avatar，使用默认头像
    }))
    router.push('/profile')  // 登录成功后跳转到 Profile 页面
  } else {
    alert('登录失败')
  }
}

</script>

<style scoped>
.login {
  text-align: center;
  margin-top: 60px;
}

input {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 200px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
button {
  padding: 8px 16px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
</style>
