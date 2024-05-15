<template>
  <div id="app">
    <GraphComponent :width="400" :height="400"/>
  </div>
</template>

<script>
import GraphComponent from './components/GraphComponent.vue';

export default {
  name: 'App',
  components: {
    GraphComponent
  }
}
</script>

<style>
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>