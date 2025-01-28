<script setup>
const emit = defineEmits(['search']);
const search = (e) => {
  emit('search', e.target.value);
};
</script>

<template>
  <form class="search-form">
    <label class="sr-only">Search</label>
    <div class="search-input-container">
      <input
        type="text"
        @input="search"
        placeholder="Search for product"
        class="search-input"
      />
    </div>
  </form>
</template>

<style>
.search-form {
  padding: var(--spacing-medium);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-color);
  
}

.search-input-container {
  position: relative;
  width: 100%;
  max-width: 200px; 
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.05);

}

.search-input {
  width: 100%;
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: var(--font-size);
  padding: var(--spacing-small) var(--spacing-medium);
  border-radius: 5px;
  transition: all 0.3s ease;
}

.search-input:hover,
.search-input:focus {
  background-color: var(--input-hover-background-color);
  border-color: var(--border-color-hover);
  outline: none; 
}

.search-input::placeholder {
  color: var(--text-color);
  opacity: 0.7;
}
</style>
