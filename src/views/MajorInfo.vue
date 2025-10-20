<template>
  <div class="major-page">
    <h2>📂 {{ majorName }} 专业资料</h2>

    <div class="section">
      <h3>📄 基本信息</h3>
      <div v-for="f in files.basic" :key="f.id" class="file-box">
        <a :href="f.url" download>{{ f.name }}</a>
      </div>
    </div>

    <div class="section">
      <h3>🎓 保研信息</h3>
      <div v-for="f in files.research" :key="f.id" class="file-box">
        <a :href="f.url" download>{{ f.name }}</a>
      </div>
    </div>

    <div class="section">
      <h3>💼 就业信息</h3>
      <div v-for="f in files.job" :key="f.id" class="file-box">
        <a :href="f.url" download>{{ f.name }}</a>
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
const files = ref({ basic: [], research: [], job: [] })

// 模拟后端请求
onMounted(async () => {
  try {
    const res = await request.get(`/files/${majorName}`)
    files.value = res.data
  } catch {
    // 模拟假数据
    files.value = {
      basic: [{ id: 1, name: '培养方案.pdf', url: '#' }],
      research: [{ id: 2, name: '保研经验分享.docx', url: '#' }],
      job: [{ id: 3, name: '就业指导.pptx', url: '#' }]
    }
  }
})
</script>

<style scoped>
.section { margin: 20px 0; }
.file-box {
  background: #fafafa;
  padding: 8px;
  margin: 5px;
  border-radius: 8px;
}
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
