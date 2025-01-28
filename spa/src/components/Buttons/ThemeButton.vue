<template>
    <label class="switch">
      <input
        type="checkbox"
        @change="toggleTheme"
        :checked="isDarkMode"
      />
      <span class="slider"></span>
    </label>
  </template>
  
  <script setup>
  import { computed, toRefs } from 'vue';
  
  const props = defineProps({
    toggleTheme: {
      type: Function,
      required: true,
    },
    theme: {
      type: String,
      required: true,
    },
  });
  const { theme } = toRefs(props);
  
  const isDarkMode = computed(() => theme.value === 'dark');
  </script>
  
  <style>
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }
  
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .slider {
    position: absolute;
    cursor: pointer;
    background-color: var(--border-color);
    border-radius: 34px;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    transition: background-color 0.4s;
  }
  
  .slider::before {
    position: absolute;
    content: '';
    height: 26px;
    width: 26px;
    background-color: var(--toggle-knob-color);
    border-radius: 50%;
    left: 4px;
    bottom: 4px;
    transition: transform 0.4s;
    box-shadow: 0 0 2px var(--box-shadow-color); /* Use theme variable */
  }
  
  input:checked + .slider::before {
    transform: translateX(26px);
  }
  
  input:checked + .slider {
    background-color: var(--border-color-hover);
  }
  
  .slider::after {
    content: '';
    position: absolute;
    height: 20px;
    width: 20px;
    top: 50%;
    transform: translateY(-50%);
    background-size: contain;
    background-repeat: no-repeat;
    transition: left 0.4s, background-image 0.4s;
  }
  
  input:not(:checked) + .slider::after {
    left: calc(100% - 24px); 
    background-image: url('@/assets/sun.svg');
  }
  
  input:checked + .slider::after {
    left: 4px; 
    background-image: url('@/assets/moon.svg');
  }
  </style>
  