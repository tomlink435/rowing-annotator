<template>
  <el-config-provider>
    <router-view />
  </el-config-provider>

</template>

<script lang="ts" setup>

const debounce = (fn, delay) => {
  let timer = null;
  return function () {
    let context = this;
    let args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  }
}

const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
  constructor(callback) {
    callback = debounce(callback, 16);
    super(callback);
  }
}

</script>

<style>
@import './assets/css/main.css';
@import './assets/css/color-dark.css';
html,
body,
#app {
  height: 100%;
  padding: 0;
  margin: 0;
}
</style>
