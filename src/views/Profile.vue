<template>
  <div class="profile">
    <div v-if="isLoggedIn" class="profile-card">
      <!-- 头像 -->
      <img :src="user.avatar || defaultAvatar" alt="头像" class="avatar" />
      <!-- 用户名 -->
      <h3>{{ user.username }}</h3>
      <!-- 欢迎语 -->
      <p>欢迎回来，祝你今天愉快 😊</p>
      <!-- 小尺寸退出按钮 -->
      <button @click="logout" class="logout-btn">退出登录</button>
    </div>

    <!-- 未登录时提示 -->
    <div v-else>
      <p>未登录，请先 <router-link to="/login">登录</router-link></p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLoggedIn = ref(false)
const user = ref(null)
const router = useRouter()
const defaultAvatar = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  const token= localStorage.getItem('token')
  if (token && savedUser) {
    isLoggedIn.value = true 
    user.value = JSON.parse(savedUser)
  } else {
    router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  router.push('/login')
}
</script>

<style scoped>
.profile {
  text-align: center;
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #f7f7f7;
}

.profile-card {
  display: inline-block;
  border-radius: 15px;
  padding: 30px 25px;
  background-color: #ffffff;
  width: 280px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  transform: translateY(-20px);
  transition: transform 0.3s ease-in-out;
}

.profile-card:hover {
  transform: translateY(-10px);
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 20px;
  object-fit: cover;
  border: 3px solid #f4f4f4;
}

h3 {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 14px;
  color: #777;
  margin-bottom: 20px;
}

.logout-btn {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #ff4d4d;
  color: #fff;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: 14px;
  width: 100%;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #cc0000;
}

.logout-btn:focus {
  outline: none;
}
</style>

