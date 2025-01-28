<template>
  <PopupMenu @close="closeModal">
    <h2 class="form-title">{{ isEditMode ? 'Edit Product' : 'Create Product' }}</h2>
    <form @submit.prevent="submitProduct" class="product-form">
      <div class="form-group">
        <label for="title">Product Title:</label>
        <input type="text" v-model="productTitle" :disabled="isEditMode" required class="form-input" />
      </div>

      <div class="form-group">
        <label for="image">Image:</label>
        <div class="custom-file-input">
          <input type="file" id="image" @change="onFileChange" accept="image/*" :disabled="isEditMode"
            class="form-input file-input" />
          <label for="image" class="form-input file-input-label" :class="{ disabled: isEditMode }"
            :aria-disabled="isEditMode ? 'true' : 'false'" tabindex="0" aria-label="Choose File">
            {{ productImage ? productImage.name : 'Choose File' }}
          </label>

        </div>
      </div>

      <div class="form-group">
        <label for="price">Price:</label>
        <input type="number" v-model="productPrice" required min="0" step="0.01" class="form-input" />
      </div>

      <div class="form-group">
        <label for="quantity">Quantity:</label>
        <input type="number" v-model="productQuantity" required min="1" class="form-input" />
      </div>

      <button type="submit" class="submit-button">Save Product</button>
    </form>
  </PopupMenu>
</template>

<script>
import PopupMenu from './Utils/PopupMenu.vue';
import keycloak from '@/auth/keycloak';

export default {
  components: {
    PopupMenu,
  },
  props: {
    mode: {
      type: String,
      default: 'create',
    },
    product: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      productTitle: this.product?.title || '',
      productPrice: this.product?.price || '',
      productQuantity: this.product?.quantity || '',
      productImage: null,
    };
  },
  computed: {
    isEditMode() {
      return this.mode === 'edit';
    },
  },
  methods: {
    onFileChange(event) {
      this.productImage = event.target.files[0];
    },
    async submitProduct() {
      const formData = new FormData();

      if (!this.isEditMode) {
        formData.append('title', this.productTitle);
        if (this.productImage) {
          formData.append('img', this.productImage);
        }
      }

      formData.append('price', this.productPrice);
      formData.append('quantity', this.productQuantity);

      const url = this.isEditMode
        ? `${import.meta.env.VITE_PRODUCTS_API}/products/${this.product.id}`
        : `${import.meta.env.VITE_PRODUCTS_API}/api/products`;

      const method = this.isEditMode ? 'PATCH' : 'POST';

      try {
        const token = keycloak.token; 
        const response = await fetch(url, {
          method,
          body: formData,
          headers: {
          'Authorization': `Bearer ${token}`
          },

        });

        if (!response.ok) {
          throw new Error(
            `${this.isEditMode ? 'Failed to update product' : 'Failed to create product'}`
          );
        }

        const result = await response.json();
        this.$emit('refresh');
        this.closeModal();
      } catch (error) {
        console.error(
          `Error ${this.isEditMode ? 'updating' : 'creating'} product:`,
          error
        );
      }
    },
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.form-title {
  font-size: 24px;
  margin-bottom: var(--spacing-medium);
  color: var(--text-color);
}

.product-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: var(--spacing-medium);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-small);
  color: var(--text-color);
}

.form-input {
  width: 100%;
  padding: var(--spacing-small);
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  border-radius: 4px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--border-color-hover);
}

.form-input:hover {
  outline: none;
  border-color: var(--border-color-hover);
}

.form-input:disabled {
  background-color: var(--disabled-background-color);
  color: var(--disabled-text-color);
  border-color: var(--border-color);
  cursor: not-allowed;
  pointer-events: none;
}

.form-input:disabled::placeholder {
  color: var(--disabled-text-color);
}

.custom-file-input {
  position: relative;
}

.file-input {
  opacity: 0;
  position: absolute;
  z-index: -1;
  width: 0;
  height: 0;
}

.file-input-label {
  display: inline-block;
  width: 100%;
  padding: var(--spacing-small);
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  border-radius: 4px;
  box-sizing: border-box;
  cursor: pointer;
}

.file-input-label:hover:not(.disabled),
.file-input-label:focus:not(.disabled) {
  border-color: var(--border-color-hover);
}

.file-input-label:focus {
  outline: none;
}

.file-input-label.disabled {
  background-color: var(--disabled-background-color);
  color: var(--disabled-text-color);
  border-color: var(--border-color);
  cursor: not-allowed;
  pointer-events: none;
}

.file-input-label.disabled:focus {
  outline: none;
  border-color: var(--border-color);
}

.submit-button {
  padding: var(--spacing-small) var(--spacing-medium);
  background-color: var(--toggle-knob-color);
  color: var(--background-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: var(--border-color-hover);
}
</style>
