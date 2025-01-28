<template>
    <div v-if="visible" class="custom-alert" :class="type">
      <button class="alert-button" @click="closeAlert">
        {{ message }}
      </button>
    </div>
  </template>
  

<script setup>
import { ref } from 'vue';

const visible = ref(false);
const message = ref('');
const type = ref('info'); 

function show(alertMessage, alertType = 'info') {
    message.value = alertMessage;
    type.value = alertType;
    visible.value = true;

    setTimeout(() => {
        visible.value = false;
    }, 6000);
}
function closeAlert() {
    visible.value = false;
}

defineExpose({ show });
</script>

<style>
.custom-alert {
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    padding: 1px 10px;
    border-radius: 5px;
    color: white;
    font-size: 20px;
    z-index: 9999;
}
.alert-button {
  width: 100%;
  padding: 10px 20px;
  background: none;
  border: none;
  font-size: 20px;
  color: inherit;
  text-align: center;
  cursor: pointer;
  border-radius: 5px;
}

.custom-alert.info {
    background-color: #455460;
}

.custom-alert.success {
    background-color: #4caf50;
}

.custom-alert.warning {
    background-color: #ff9800;
}

.custom-alert.error {
    background-color: #f44336;
}
</style>