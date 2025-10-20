<template>
  <div class="register">
    <h2>📝 注册</h2>
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" type="password" placeholder="密码" />
    <input v-model="confirmPassword" type="password" placeholder="确认密码" />
    <button @click="register">注册</button>
    <p>已有账号？<router-link to="/login">登录</router-link></p> <!-- 跳转到登录页面 -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../api/request'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const router = useRouter()

const register = async () => {
  if (password.value !== confirmPassword.value) {
    alert('密码不一致！')
    return
  }

  try {
    await request.post('/auth/register', {
      username: username.value,
      password: password.value
    })
    alert('注册成功！')
    router.push('/login')
  } catch (err) {
    alert('注册失败')
  }
}
</script>

<style scoped>
.register {
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
