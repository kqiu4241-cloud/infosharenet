<template>
  <div class="home">
    <h2>📚 请选择你的专业进入资料区</h2>
    <div class="major-grid">
      <router-link
        v-for="major in majors"
        :key="major.name"
        :to="`/major/${major.name}`"
        class="major-card"
      >
        <h3>{{ major.name }}</h3>
        <p>{{ major.desc }}</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
const majors = [
  { name: '通信工程', desc: '信号与系统、通信原理、无线网络' },
  { name: '信息工程', desc: '信号处理、智能通信、嵌入式系统' },
  { name: '集成电路', desc: 'VLSI、芯片设计、EDA工具' },
  { name: '电子信息', desc: '图像处理、嵌入式开发、计算机视觉' }
]
</script>

<style scoped>
.major-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}
.major-card {
  width: 220px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  text-align: center;
  transition: 0.3s;
  text-decoration: none;
  color: black;
}
.major-card:hover {
  transform: translateY(-5px);
  background: #e3f2fd;
}
</style>
