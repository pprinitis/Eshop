<template>
  <button :class="['delete-button']" @click="handleDelete">
    <img :src="trashLogo" alt="Delete" class="delete-icon" />
  </button>
</template>


<script setup>
import trashLogo from '@/assets/trash.svg';
import { defineEmits } from 'vue';

const emit = defineEmits(['delete']);

const props = defineProps({
  productId: {
    type: Number,
    required: true,
  },
});

const handleDelete = () => {
  emit('delete', props.productId); 
};
</script>

<style scoped>

.action-button {
  padding: calc(var(--spacing-small) / 2) var(--spacing-small);
  background-color: var(--border-color-hover);
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: var(--font-size);
  min-width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;

}

.action-button:hover {
  background-color: var(--submit-button-hover-background-color);
}

.delete-button {
  background-color: var(--accent-red-color);
  padding: calc(var(--spacing-small) / 2) var(--spacing-small);
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  min-width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.delete-button:hover {
  background-color: var(--accent-red-color-hover);
}

.delete-button:active {
  background-color: var(--accent-red-color-hover);
}

.delete-icon {
  width: 40px;
  height: 25px;
  filter: var(--icon-filter);
}
</style>
