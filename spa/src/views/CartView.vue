<script setup>
import { onMounted, ref, computed } from "vue";
import TableContainer from "@/components/Tables/TableContainer.vue";
import PlaceOrderButton from "@/components/Buttons/PlaceOrderButton.vue";
import ProductTableRow from "@/components/Tables/ProductTableRow.vue";
import DeleteButton from "@/components/Buttons/DeleteButton.vue";
import PlusIcon from "@/assets/plus.svg";
import MinusIcon from "@/assets/minus.svg";
import keycloak from '@/auth/keycloak';

const items = ref([]);
const loading = ref(true);
const error = ref(null);

const initializeCart = () => {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  localStorage.setItem("cart", JSON.stringify(cart));
};
onMounted(async () => {
  initializeCart();
  fetchProducts();
});

const fetchProducts = async () => {
  loading.value = true;
  try {
    const cartData = JSON.parse(localStorage.getItem("cart")) || [];
    items.value = cartData;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};


const totalPrice = computed(() => {
  return items.value.reduce((total, item) => {
    const itemTotal = parseFloat(item.price) * parseInt(item.quantity, 10);
    return total + itemTotal;
  }, 0);
});

const updateQuantity = (id, quantity) => {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const updatedCart = cart.map((item) => {
    if (item.id === id) {
      return { ...item, quantity: Math.max(1, quantity) };
    }
    return item;
  });
  localStorage.setItem("cart", JSON.stringify(updatedCart)); 
  items.value = updatedCart; 
};


const handlePlaceOrder = async () => {
  const totalPriceValue = totalPrice.value;
  const orderData = {
    products: items.value.map((item) => ({
      product_id: item.id,
      title: item.title,
      amount: item.quantity,
    })),
    total_price: parseFloat(totalPriceValue)
  };

  try {
    const token = keycloak.token;
    const response = await fetch(`${import.meta.env.VITE_ORDERS_API}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(orderData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Failed to create order");
    }
    items.value = []
    localStorage.removeItem('cart')
  } catch (error) {
    console.error("Order failed:", error.message);
    alert("There was an issue placing your order.");
  }
};

const removeProduct = async (productId) => {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const updatedCart = cart.filter((cartItem) => cartItem.id !== productId);
  localStorage.setItem("cart", JSON.stringify(updatedCart)); 
  items.value = updatedCart; 
};


</script>
<template>
  <TableContainer :headers="['Title', 'Image', 'Price', 'Quantity', 'Action']" :items="items" :loading="loading"
    :error="error" row-key="id">
    <template #buttons>
      <PlaceOrderButton :total-price="totalPrice" @order="handlePlaceOrder" />
    </template>
    <template #row="{ item }">
      <ProductTableRow :item=item :hide-id="true" :hide-quantity="true" />
      <td>
        <div class="action-buttons">
          <button @click="updateQuantity(item.id, item.quantity - 1)" class="icon-button">
            <img :src="MinusIcon" alt="Decrease quantity" class="quantity-icon" />
          </button>
          <input type="number" :value="item.quantity"
            @input="(e) => updateQuantity(item.id, parseInt(e.target.value, 10))" class="quantity-input" />
          <button @click="updateQuantity(item.id, item.quantity + 1)" class="icon-button">
            <img :src="PlusIcon" alt="Increase quantity" class="quantity-icon" />
          </button>
        </div>
      </td>
      <td>
        <div class="action-buttons">

          <DeleteButton :productId="item.id" @delete="removeProduct" />
        </div>
      </td>
    </template>

  </TableContainer>
</template>

<style scoped>
.quantity-input {
  -webkit-appearance: none; 
  -moz-appearance: textfield; 
  appearance: textfield;
  width: 3rem;
  text-align: center;
  background-color: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: var(--spacing-small);
}

.quantity-input::-webkit-inner-spin-button,
.quantity-input::-webkit-outer-spin-button {
  -webkit-appearance: none; 
  margin: 0;
}

.quantity-input:hover {
  background-color: var(--input-hover-background-color);
}

.icon-button {
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--spacing-small);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.icon-button:hover {
  background-color: var(--border-color-hover);
  border-radius: 4px;
}

.quantity-icon {
  width: 20px;
  height: 20px;
  filter: var(--icon-filter);
}

:host-context(.dark-theme) {
  .quantity-input {
    border: 1px solid var(--border-color);
  }
  .icon-button:hover {
    background-color: var(--submit-button-hover-background-color);
  }
}
</style>
