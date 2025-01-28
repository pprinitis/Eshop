<template>
  <div class="container">
    <div class="content">
      <div v-if="$slots.buttons" class="top-buttons">
        <slot name="buttons" />
      </div>

      <div v-if="loading" class="text-center">Loading...</div>
      <div v-else-if="error" class="text-center error-message">{{ error }}</div>
      <div v-else-if="!items.length" class="text-center">No data found</div>

      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header" class="table-header">
                <slot name="header" :header="header">{{ header }}</slot>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item[rowKey]" class="table-row">
              <slot name="row" :item="item" />
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  headers: { type: Array, required: true },
  items: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: null },
  rowKey: { type: String, required: true },
});
</script>

<style>
.container {
  padding: 0;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

@media (min-width: 768px) {
  .container {
    padding: var(--spacing-medium);
  }
}

.content {
  position: relative;
  border: 1px solid var(--border-color);
  color: var(--text-color);
  border-radius: 8px;
  padding: var(--spacing-small);
  display: flex;
  flex-direction: column;
}

.top-buttons {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  margin-bottom: var(--spacing-small);
  margin-left: 5px;

}

@media screen and (max-width: 600px) {

  .top-buttons {
    justify-content: center;
    margin-left: 0;
  }
}

.top-buttons button {
  margin-right: var(--spacing-small);
}

.text-center {
  text-align: center;
  padding: var(--spacing-small);
}

.error-message {
  color: var(--accent-red-color);
}

.table-wrapper {
  background-color: rgba(0, 0, 0, 0.01);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 1px 2px 3px rgba(0, 0, 0, 0.1);
  margin-top: var(--spacing-small);

}

.data-table {
  width: 100%;
  border-collapse: collapse;
}


.data-table th,
.data-table td {

  font-size: var(--font-size);
  color: var(--text-color);
  padding: var(--spacing-small);
  vertical-align: middle;
  text-align: center;
}

.data-table th {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-color);
  font-weight: bold;
  text-transform: uppercase;
}

.data-table th:first-child {
  border-top-left-radius: 8px;

}

.data-table th:last-child {
  border-top-right-radius: 8px;

}

.data-table tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}

.data-table tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
}

.data-table th {
  background-color: rgba(0, 0, 0, 0.1);
  color: var(--text-color);
  font-weight: bold;
}

.data-table tr:hover {
  background-color: rgba(0, 0, 0, 0.03);
  transition: background-color 0.3s ease;
}

.table-image {
  display: block;
  max-width: 80px;
  max-height: 80px;
  width: 100%;
  object-fit: cover;
  border-radius: 8px;
  margin: 0 auto;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: var(--spacing-small);
}

.top-buttons {
  display: flex;
  justify-content: start;
  gap: var(--spacing-small);
}
</style>
