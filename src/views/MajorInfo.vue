<template>
  <div class="major-page">
    <h2>📂 {{ majorName }} 专业资料</h2>

    <!-- 基本信息 -->
    <div class="section">
      <h3>📄 基本信息</h3>
      <div v-if="files.basic.length === 0">暂无文件</div>
      <div v-for="f in files.basic" :key="f.name" class="file-box">
        <a :href="`${backendBase}${f.url}`" target="_blank" download>{{ f.name }}</a>
      </div>
    </div>

    <!-- 保研信息 -->
    <div class="section">
      <h3>🎓 保研信息</h3>
      <div v-if="files.research.length === 0">暂无文件</div>
      <div v-for="f in files.research" :key="f.name" class="file-box">
        <a :href="`${backendBase}${f.url}`" target="_blank" download>{{ f.name }}</a>
      </div>
    </div>

    <!-- 就业信息 -->
    <div class="section">
      <h3>💼 就业信息</h3>
      <div v-if="files.job.length === 0">暂无文件</div>
      <div v-for="f in files.job" :key="f.name" class="file-box">
        <a :href="`${backendBase}${f.url}`" target="_blank" download>{{ f.name }}</a>
      </div>
    </div>

    <router-link v-if="isLoggedIn" to="/upload" class="upload-btn">上传资料</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../api/request'

const route = useRoute()
const majorName = route.params.name
const isLoggedIn = !!localStorage.getItem('token')

// ✅ 这里用虚拟机 IP
const backendBase = 'http://192.168.187.135:5000'

const files = ref({ basic: [], research: [], job: [] })

const loadFiles = async () => {
  try {
    const res = await request.get(`/files/${majorName}`)
    console.log('后端返回:', res) // 这里 res 直接是数据对象，而不是 res.data
    files.value = res
  } catch (err) {
    console.error('加载失败:', err)
    alert('无法加载文件列表，请检查后端是否运行')
  }
}

onMounted(loadFiles)
</script>

<style scoped>
.section { margin: 20px 0; padding: 10px; background: #fafafa; border-radius: 10px; }
.file-box { padding: 8px; margin: 5px 0; background: white; border-radius: 6px; }
.file-box a { color: #007bff; text-decoration: none; }
.file-box a:hover { text-decoration: underline; }
.upload-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 15px;
  background: #007bff;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
}
</style>
