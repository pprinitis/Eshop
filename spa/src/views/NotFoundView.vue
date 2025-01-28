<script setup>
import { RouterLink } from 'vue-router';
</script>
<template >
    <section class="text-center flex flex-col justify-center items-center h-96">
      <i class="pi pi-exclamation-triangle text-red-500 text-7xl md:text-8xl py-5"></i>
      <h1 class="text-6xl font-bold mb-4">404 Not Found</h1>
      <p class="text-xl mb-5">This page does not exist or you dont have access</p>
      <RouterLink
        to="/"
        class="text-white bg-gray-800 hover:bg-gray-900 rounded-md px-3 py-2 mt-4"
        >Home</RouterLink>
    </section>


</template>