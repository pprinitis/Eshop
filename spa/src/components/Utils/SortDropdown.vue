<template>
    <div class="dropdown-container">
      <select id="sortOptions" v-model="selected" @change="emitSelection" class="dropdown-select">
        <option value="" disabled>Sort By</option>
        <option value="">Sort: Default</option>
        <option value="title-asc">Sort: Title Ascending</option>
        <option value="title-desc">Sort: Title Descending</option>
        <option value="price-asc">Sort: Price Ascending</option>
        <option value="price-desc">Sort: Price Descending</option>
        <option value="quantity-asc">Sort: Quantity Ascending</option>
        <option value="quantity-desc">Sort: Quantity Descending</option>

      </select>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const selected = ref("");
  const emit = defineEmits(["sort"]);
  const emitSelection = () => {
    emit("sort", selected.value);
  };
  </script>
  
  <style scoped>
  .dropdown-container {
    
    display: flex;
    align-items: center;
    
  }
  
  .dropdown-select {
    padding: 12px var(--spacing-medium);
    font-size: var(--font-size);
    color: var(--text-color);
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.05);

  }
  
  .dropdown-select option {
    background-color: var(--background-color);

    font-size: var(--font-size);
    color: var(--text-color);
  }
  
  .dropdown-select:hover {
    background-color: rgb(0,0,0,0.05);
  }
  </style>
  