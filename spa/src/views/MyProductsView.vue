<script setup>
import { onMounted, ref } from "vue";

import TableContainer from "@/components/Tables/TableContainer.vue";
import CreateProduct from "@/components/CreateProduct.vue";
import DeleteButton from "@/components/Buttons/DeleteButton.vue";
import ProductTableRow from "@/components/Tables/ProductTableRow.vue";
import keycloak from '@/auth/keycloak';

const items = ref([]);
const loading = ref(true);
const error = ref(null);
const showModal = ref(false);
const modalMode = ref("create"); 
const editableProduct = ref(null); 

onMounted(() => {
  fetchProducts();
});

const fetchProducts = async () => {
  loading.value = true; 

  try {
    const token = keycloak.token; 
    const response = await fetch(`${import.meta.env.VITE_PRODUCTS_API}/myproducts`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) throw new Error("Failed to fetch products");
    items.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false; 
  }
};

const removeProduct = async (productId) => {

  if (confirm('Are you sure you want to delete this product?')) {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_PRODUCTS_API}/products/${productId}`,
        {
          headers: {
          'Authorization': `Bearer ${token}`
          },
          method: 'DELETE',
        }
      );
      if (response.ok) {
        refresh();
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const updatedCart = cart.filter(cartItem => cartItem.id !== productId);
        localStorage.setItem('cart', JSON.stringify(updatedCart));

        window.$alert("Product deleted", "error");
      } else {
        const errorData = await response.json();
        console.error('Error deleting product:', errorData.message);
      }
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  }
};

const openModal = (mode = "create", product = null) => {
  modalMode.value = mode;
  editableProduct.value = product; 
  showModal.value = true; 
};

const closeModal = () => {
  showModal.value = false; 
};

const refresh = () => {
  fetchProducts();
};
</script>

<template>
  <TableContainer :headers="['Id', 'Title', 'Image', 'Price', 'In stock', 'Actions']" :items="items" :loading="loading"
    :error="error" row-key="id">
    <template #buttons>
      <button class="add-button" @click="openModal('create')">
        Add Product
      </button>
    </template>

    <template #row="{ item }">
      <ProductTableRow :item=item />

      <td>
        <div class="action-buttons">
          <button @click="openModal('edit', item)" class="action-button edit-button">
            Edit
          </button>
          <DeleteButton :productId="item.id" @delete="removeProduct" />
        </div>
      </td>
    </template>
  </TableContainer>

  <CreateProduct v-if="showModal" :mode="modalMode" :product="editableProduct" @close="closeModal" @refresh="refresh" />
</template>
<style scoped>
.add-button {
  padding: calc(var(--spacing-small) / 2) var(--spacing-medium);
  background-color: var(--background-color);
  color: var(--text-color);
  border: 2px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
}

.add-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.edit-button {
  padding: calc(var(--spacing-small) / 2) var(--spacing-small);
  background-color: var(--background-color);
  color: var(--text-color);
  border: 2px solid var(--border-color);
  border-radius: 4px;
  margin-right: var(--spacing-small);
  cursor: pointer;
  width: 60px;
}

.edit-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>
