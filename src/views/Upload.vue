<template>
  <div class="upload">
    <h2>📤 上传资料</h2>

    <div>
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
    </div>

    <input type="file" @change="onFileChange" />
    <button @click="upload">上传</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'

const router = useRouter()

const major = ref('信息工程')
const category = ref('basic')
const file = ref(null)

// 选择文件
const onFileChange = e => {
  file.value = e.target.files[0]
}

// 上传文件
const upload = async () => {
  if (!file.value) return alert('请选择文件')
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('major', major.value)
  formData.append('category', category.value)

  try {
    // 注意：后端接口是 /upload，不是 /files/upload
    await request.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    alert('上传成功！')

    // 跳转到对应专业的资料页
    router.push(`/major/${major.value}`)
  } catch (err) {
    alert('上传失败或后端未连接')
    console.error(err)
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
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
</style>
