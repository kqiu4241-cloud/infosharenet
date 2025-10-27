<template>
  <div class="profile">
    <h2>👤 个人主页</h2>

    <div v-if="user" class="profile-card">
      <img :src="user.avatar || defaultAvatar" alt="头像" class="avatar" />
      <h3>{{ user.username }}</h3>
      <p>欢迎登录，祝你今天愉快 😊</p>
      <button @click="logout">退出登录</button>
    </div>

    <div v-else>
      <p>未登录，请先 <router-link to="/login">登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()
const defaultAvatar = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
  }
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.profile {
  text-align: center;
  margin-top: 80px;
}

.profile-card {
  display: inline-block;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 20px;
  background-color: #f9f9f9;
  width: 280px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #ff4d4d;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #cc0000;
}
</style>
