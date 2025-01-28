<script setup>
import { ref, computed ,onMounted} from 'vue';
import NavBar from './components/NavBar.vue';
import CustomAlert from './components/Utils/CustomAlert.vue';

const theme = ref('light'); 

const themeClass = computed(() => {
  return theme.value === 'dark' ? 'dark-theme' : '';
});

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
}

const alertRef = ref(null);

onMounted(() => {
  if (alertRef.value && alertRef.value.show) {
    window.$alert = alertRef.value.show;
  }
});

</script>

<template>
  <div :class="themeClass" id="app">
    <NavBar :toggleTheme="toggleTheme" :theme="theme" />

    <main id="main-content">
      <RouterView />
      <CustomAlert ref="alertRef" />
    </main>
  </div>
</template>


<style>
@import './assets/theme.css';

#app {
  background-color: var(--background-color);
  color: var(--text-color);
  min-height: 100vh;
}

body,
html {
  margin: 0;
  padding: 0;
}

#main-content {
  padding: var(--spacing-medium);
}
</style>