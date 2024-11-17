<template>
  <div id="app">
    <!-- Router View to dynamically load the correct page based on the route -->
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
