<script setup>
import { ref, defineEmits, watch } from "vue";
import cartSvg from "@/assets/cart.svg"
const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const handleAddClick = () => {
  const cartItem = {
    id: props.item.id,
    title: props.item.title,
    img: props.item.img,
    price: props.item.price,
    quantity: 1,
  };
  const cart = JSON.parse(localStorage.getItem('cart')) || [];

  const existingItemIndex = cart.findIndex(cartItem => cartItem.id === props.item.id);
  if (existingItemIndex > -1) {
    window.$alert("Product already in cart", "info");
  } else {
    cart.push(cartItem);
    localStorage.setItem('cart', JSON.stringify(cart));
    window.$alert("Item added to cart", "success");
  }
};
</script>

<template>
  <button
    class="add-to-cart-btn"
    @click.prevent="handleAddClick"
    :disabled="props.item.quantity === 0"
  >
    <img :src="cartSvg" alt="Cart Icon" class="cart-icon" />
    Add to Cart
  </button>
</template>

<style scoped>
.add-to-cart-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-small);
  padding: var(--spacing-small) var(--spacing-medium);
  font-size: var(--font-size);
  font-weight: bold;
  color: var(--text-color);
  background-color: var(--background-color);
  border: 2px solid var(--border-color);
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.add-to-cart-btn img {
  width: 25px;
  height: 25px;
  filter: var(--icon-filter);
  transition: filter 0.3s ease;
}

.add-to-cart-btn:hover {
  background-color: rgb(0,0,0,0.3);
  color: var(--text-color);
  border-color: var(--border-color-hover);
}

.add-to-cart-btn:disabled {
  background-color: var(--disabled-background-color);
  color: var(--disabled-text-color);
  cursor: not-allowed;
  border-color: var(--border-color);
}

.add-to-cart-btn .cart-icon {
  margin-right: var(--spacing-small);
  filter: var(--icon-filter);
}
</style>