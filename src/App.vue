<template>
  <div id="app">
    <header class="header">
      <h1>🎓 23级信息工程学院资料网</h1>
      <nav>
        <router-link to="/">首页</router-link> |
        <router-link to="/login">登录</router-link> |
        <router-link to="/upload">上传资料</router-link>
      </nav>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: "Microsoft YaHei", sans-serif;
  background: #f8f9fa;
}
.header {
  text-align: center;
  padding: 20px;
  background: #0059b3;
  color: white;
}
.header a {
  color: #fff;
  margin: 0 10px;
  text-decoration: none;
}
.main {
  padding: 20px;
}
</style>
