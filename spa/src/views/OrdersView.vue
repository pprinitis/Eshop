<script setup>
import TableContainer from "@/components/Tables/TableContainer.vue";
import keycloak from '@/auth/keycloak';
import { onMounted, ref } from "vue";

const items = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  fetchOrders();
});

const fetchOrders = async () => {
  loading.value = true; 

  try {
    const token = keycloak.token;
    const responce = await fetch(`${import.meta.env.VITE_ORDERS_API}/orders`,{
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!responce.ok) throw new Error("Failed to fetch products");
    items.value = await responce.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false; 
  }
};
</script>
<template>
  <TableContainer :headers="['Id', 'Status', 'Total price', 'Products']" :items="items" :loading="loading"
    :error="error" row-key="id">
    <template #row="{ item }">
      <td >{{ item.id }}</td>
      <td >{{ item.status }}</td>
      <td>{{ item.total_price.toFixed(2) }}</td>
      <td >
        <ul class="products-list">
          <li 
            v-for="product in item.products" 
            :key="product.product_id" 
            class="product-item"
          >
            {{ product.amount }} x {{ product.title }}
          </li>
        </ul>
      </td>

    </template>
  </TableContainer>

</template>
<style scoped>
.products-list {
  list-style: none;
  padding: 0;
  margin: 0; 
}

.product-item {
  padding: var(--spacing-small) 0;
  font-size: var(--font-size); 
  color: var(--text-color); 
  border-bottom: 1px dashed var(--border-color); 
}

.product-item:last-child {
  border-bottom: none; 
}
</style>
