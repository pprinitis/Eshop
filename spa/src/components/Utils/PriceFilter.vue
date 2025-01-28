<template>
  <form class="price-filter">
    <div class="price-border">
      <div class="price-elements">
        <div class="price-input-container">
          <input id="minPrice" type="number" v-model="minPrice" placeholder="Min price" class="price-input" />
        </div>
        <div class="price-input-container">
          <input id="maxPrice" type="number" v-model="maxPrice" placeholder="Max price" class="price-input" />
        </div>
      </div>
      <div class="price-elements">
        <button type="button" class="apply-button" @click="applyFilter">Apply</button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref } from "vue";

const minPrice = ref("");
const maxPrice = ref("");
const emit = defineEmits(["update-price"]);

const applyFilter = () => {
  const range = {
    min: minPrice.value ? parseFloat(minPrice.value) : null,
    max: maxPrice.value ? parseFloat(maxPrice.value) : null,
  };
  emit("update-price", range);
};
</script>

<style scoped>
.price-filter {
  padding: calc(var(--spacing-medium) - 2px);
  display: flex;
  align-items: center;
  gap: var(--spacing-medium);
  background-color: var(--background-color);
}

.price-border {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  gap: var(--spacing-medium);
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  flex-wrap: wrap;
  padding: 0;
}

.price-input-container {
  position: relative;
  width: 100%;
  max-width: 180px;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.05);
}

.price-elements {
  display: flex;
  gap: var(--spacing-medium);
}

.price-input {
  display: flex;
  width: 100%;
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: var(--font-size);
  padding: var(--spacing-small) var(--spacing-medium);
  border-radius: 5px;
  transition: all 0.3s ease;
}

.price-input:hover,
.price-input:focus {
  background-color: var(--input-hover-background-color);
  border-color: var(--border-color-hover);
  outline: none;
}

.price-input::placeholder {
  color: var(--text-color);
  opacity: 0.7;
}

.apply-button {
  margin: 0;
  display: flex;
  padding: var(--spacing-small) var(--spacing-medium);
  font-size: var(--font-size);
  font-weight: 500;
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.apply-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
