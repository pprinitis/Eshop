<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">
        <img src="@/assets/close.svg" alt="Close" />
      </button>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--background-color);
  color: var(--text-color);
  padding: var(--spacing-medium);
  border-radius: 8px;
  position: relative;
  max-width: 500px;
  width: 90%;
  box-sizing: border-box;
  border: 1px solid var(--border-color);
}

.close-btn {
  position: absolute;
  top: calc(var(--spacing-small) * 2);
  right: var(--spacing-medium);
  background: var(--accent-red-color);
  padding: 2px;
  border-radius: 20%;
  cursor: pointer;
}

.close-btn img {
  width: 28px;
  height: 28px;
  filter: var(--icon-filter, none); 
}

.close-btn:hover {
  background: var(--accent-red-color-hover);
}

</style>
