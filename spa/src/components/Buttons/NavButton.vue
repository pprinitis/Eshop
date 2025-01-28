<template>
  <RouterLink
    :to="to"
    :class="['nav-button', isActive ? 'active' : '', disabled ? 'disabled' : '']"
    :aria-disabled="disabled"
    @click.prevent="handleClick"
    :title="disabled ? hint : ''"  

  >
    {{ label }}
  </RouterLink>
</template>

<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { watch, ref} from 'vue';

const props = defineProps({
  to: {
    type: String,
    required: true, 
  },
  label: {
    type: String,
    required: true, 
  },
  disabled: {
    type: Boolean,
    default: true,
  },
  hint: {
    type: String,
    default: 'You do not have permission to access this page.',  // Default hint message
  },
});

const route = useRoute();

const isActiveLink = () => {
  return route.path === props.to;
};
const isActive = ref(isActiveLink());

watch(() => route.path, () => {
  isActive.value = isActiveLink();
});


const handleClick = (event) => {
  if (props.disabled) {
    event.preventDefault();
    event.stopImmediatePropagation();
  }
};
</script>

<style scoped>

.nav-button {
  padding: var(--spacing-small);
  padding-left: var(--spacing-medium);
  padding-right: var(--spacing-medium);

  margin: 0 var(--spacing-small);
  font-size: var(--font-size);
  text-decoration: none;
  color: var(--text-color);
  background-color: var(--background-color);
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.05); /* Optional shadow for depth */  
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
  
}

.nav-button:hover {
  background-color: var(--border-color-hover);
  color: var(--text-color);
}

.nav-button.active {
  background-color: var(--border-color);
  color: var(--text-color);
}

.disabled {
  pointer-events: none;
  opacity: 0.5; /* or any other styling to indicate it's disabled */
}

</style>
