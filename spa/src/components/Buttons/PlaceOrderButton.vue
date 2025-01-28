<script setup>

const props = defineProps({
  totalPrice: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["order"]);

const handlePlaceOrder = () => {
  if (props.totalPrice > 0) {
    emit("order"); 
  }
};
</script>

<template>
  <div class="checkout-container">
    <div class="total-container">
      <span class="total-price">
        Total: {{ totalPrice.toFixed(2) }} €
      </span>
    </div>
    <div class="button-container">
      <button
        @click.prevent="handlePlaceOrder"
        :disabled="totalPrice <= 0"
        class="place-order-button"
      >
        Place Order
      </button>
    </div>
  </div>
</template>

<style scoped>
.checkout-container {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  padding: var(--spacing-medium);
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.05); 
  margin-top: var(--spacing-small);
}

.total-container {
  flex-grow: 1;
  text-align: left;
  margin-right: var(--spacing-medium);
}

.total-price {
  font-size: var(--font-size);
  font-weight: 600;
  color: var(--text-color);
}

.button-container {
  text-align: right;
}

.place-order-button {
  background-color: var(--border-color-hover);
  color: var(--text-color);
  font-size: var(--font-size);
  padding: calc(var(--spacing-small) / 2) var(--spacing-medium);
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s, transform 0.2s;
}

.place-order-button:hover {
  background-color: var(--submit-button-hover-background-color);
}

.place-order-button:disabled {
  background-color: var(--disabled-background-color);
  color: var(--disabled-text-color);
  opacity: 0.5;
  cursor: not-allowed;
}

.place-order-button:active {
  transform: scale(0.98); /* Slightly reduce size */
}
</style>
