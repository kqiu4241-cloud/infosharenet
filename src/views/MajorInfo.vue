<template>
  <div class="major-page">
    <h2>📂 {{ majorName }} 专业资料</h2>

    <!-- 基本信息 -->
    <div class="section">
      <h3>📄 基本信息</h3>
      <div v-if="files.basic.length === 0">暂无文件</div>
      <div class="file-list">
        <div v-for="f in files.basic" :key="f.name" class="file-box">
          <a :href="`${backendBase}${f.url}`" target="_blank">{{ f.name }}</a>
        </div>
      </div>
    </div>

    <!-- 保研信息 -->
    <div class="section">
      <h3>🎓 保研信息</h3>
      <div v-if="files.research.length === 0">暂无文件</div>
      <div class="file-list">
        <div v-for="f in files.research" :key="f.name" class="file-box">
          <a :href="`${backendBase}${f.url}`" target="_blank">{{ f.name }}</a>
        </div>
      </div>
    </div>

    <!-- 就业信息 -->
    <div class="section">
      <h3>💼 就业信息</h3>
      <div v-if="files.job.length === 0">暂无文件</div>
      <div class="file-list">
        <div v-for="f in files.job" :key="f.name" class="file-box">
          <a :href="`${backendBase}${f.url}`" target="_blank">{{ f.name }}</a>
        </div>
  </div>
</div>

<div class="search-bar">
  <input v-model="keyword" placeholder="输入关键字..." />
  <select v-model="selectedCategory">
    <option value="">全部类别</option>
    <option value="basic">基本信息</option>
    <option value="research">保研信息</option>
    <option value="job">就业信息</option>
  </select>
  <select v-model="selectedMajor">
    <option value="">全部专业</option>
    <option value="信息工程">信息工程</option>
    <option value="通信工程">通信工程</option>
    <option value="集成电路">集成电路</option>
    <option value="电子信息">电子信息</option>
  </select>
  <button @click="searchFiles">搜索</button>
  <button @click="loadFiles">重置</button>
</div>

<div v-if="searchResults.length" class="search-results">
  <h2>🔍 搜索结果</h2>
  <ul>
    <li v-for="file in searchResults" :key="file.url">
      <!-- ✅ 直接使用 file.url，不再拼 backendBase -->
      <!-- ✅ 去掉 download 属性（因为跨域下载会被 Chrome 拦截） -->
      <a
        :href="encodeURI(file.url)"
        target="_blank"
        rel="noopener noreferrer"
      >
        {{ file.name }}
      </a>
      <span class="meta">（{{ file.major }} - {{ file.category }}）</span>
    </li>
  </ul>
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

const keyword = ref('')
const selectedCategory = ref('')
const selectedMajor = ref('')
const searchResults = ref([])

const searchFiles = async () => {
  if (!keyword.value.trim()) {
    alert('请输入关键字')
    return
  }

  try {
    const res = await request.get('/files/search', {
      params: {
        keyword: keyword.value,
        category: selectedCategory.value,
        major: selectedMajor.value
      }
    })
    searchResults.value = res
  } catch (err) {
    console.error('搜索失败：', err)
  }
}


onMounted(loadFiles)
</script>

<style scoped>
.section {
  margin: 20px 0;
  padding: 10px;
  background: #fafafa;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0,0,0,0.05);
}

/* 滚动容器 */
.file-list {
  max-height: 250px; /* ⚙️ 你可以改成 300px、400px 等 */
  overflow-y: auto;
  padding-right: 8px;
  margin-top: 8px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fff;
}

/* 优化滚动条 */
.file-list::-webkit-scrollbar {
  width: 8px;
}
.file-list::-webkit-scrollbar-thumb {
  background-color: #bbb;
  border-radius: 4px;
}
.file-list::-webkit-scrollbar-thumb:hover {
  background-color: #999;
}

/* 文件块样式 */
.file-box {
  padding: 8px;
  margin: 5px 0;
  background: white;
  border-radius: 6px;
  border-bottom: 1px solid #f0f0f0;
}
.file-box a {
  color: #007bff;
  text-decoration: none;
}
.file-box a:hover {
  text-decoration: underline;
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
.search-results {
  margin-top: 20px;
  text-align: left;
}
.search-results h2 {
  font-size: 20px;
  margin-bottom: 10px;
}
.search-results ul {
  list-style: none;
  padding: 0;
}
.search-results li {
  margin: 6px 0;
}
.search-results a {
  color: #007bff;
  text-decoration: none;
}
.search-results a:hover {
  text-decoration: underline;
}
.search-results .meta {
  color: #888;
  margin-left: 10px;
}

</style>
