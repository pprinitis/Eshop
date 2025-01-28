<script setup>
import { onMounted, ref } from "vue";
import SearchForm from "@/components/Utils/SearchForm.vue";
import TableContainer from "@/components/Tables/TableContainer.vue";
import AddToCartButton from "@/components/Buttons/AddToCartButton.vue";
import ProductTableRow from "@/components/Tables/ProductTableRow.vue";
import PriceFilter from "@/components/Utils/PriceFilter.vue";
import SortDropdown from "@/components/Utils/SortDropdown.vue";
const items = ref([]);
const loading = ref(true);
const error = ref(null);
const searchParams = ref({ title: '' });

onMounted(async () => {
  fetchProducts();
});

const fetchProducts = async () => {
  loading.value = true;

  try {
    const query = new URLSearchParams(searchParams.value).toString(); 
    const response = await fetch(`${import.meta.env.VITE_PRODUCTS_API}/products?${query}`);
    if (!response.ok) throw new Error("Failed to fetch products");
    items.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false; 
  }
};

const handleSearch = (search) => {
  searchParams.value.title = search; 
  fetchProducts(); 
}

const handlePriceFilter = (range) => {
  searchParams.value.min_price = range.min;
  searchParams.value.max_price = range.max;
  fetchProducts();
};


const handleSort = (sortOption) => {
  searchParams.value.sort = sortOption;
  fetchProducts();
};

</script>

<template>
  <TableContainer :headers="['Id', 'Title', 'Image', 'Price', 'In stock', 'Actions']" :items="items" :loading="loading"
    :error="error" row-key="id">
    <template #buttons>
      <SearchForm @search="handleSearch" />
      <SortDropdown @sort="handleSort"/>
      <PriceFilter @update-price="handlePriceFilter" />
    </template>
    <template #row="{ item }">
      <ProductTableRow :item=item />
      <td>
        <div class="action-buttons">

          <AddToCartButton :item="item" />

        </div>
      </td>
    </template>
</TableContainer>
</template>
