<template>
  <div class="upload">
    <h2>📤 上传资料</h2>
    <select v-model="major">
      <option>信息工程</option>
      <option>通信工程</option>
      <option>集成电路</option>
      <option>电子信息</option>
    </select>

    <select v-model="category">
      <option value="basic">基本信息</option>
      <option value="research">保研信息</option>
      <option value="job">就业信息</option>
    </select>

    <input type="file" @change="onFileChange" />
    <button @click="upload">上传</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../api/request'

const major = ref('信息工程')
const category = ref('basic')
const file = ref(null)

const onFileChange = e => {
  file.value = e.target.files[0]
}

const upload = async () => {
  if (!file.value) return alert('请选择文件')
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('major', major.value)
  formData.append('category', category.value)

  try {
    await request.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    alert('上传成功！')
  } catch {
    alert('模拟上传成功！（后端未连接）')
  }
}
</script>

<style scoped>
.upload {
  text-align: center;
  margin-top: 40px;
}
select, input, button {
  margin: 10px;
  padding: 8px;
}
button {
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
}
</style>
