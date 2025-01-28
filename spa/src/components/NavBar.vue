<script setup>
import NavButton from '@/components/Buttons/NavButton.vue';
import ThemeButton from './Buttons/ThemeButton.vue';
import User from './User.vue';
import keycloak from '@/auth/keycloak';
import { ref, onMounted } from 'vue';

const props = defineProps({
  toggleTheme: {
    type: Function,
    required: true,
  },
  theme: {
    type: String,
    required: true,
  },
});

const user = ref({
  name: "Guest",
  isLoggedIn: false,
  role: "guest"
});

function handleAuth() {
  if (user.value.isLoggedIn) {
    keycloak.logout({ redirectUri: window.location.origin });
  } else {
    keycloak.login({ redirectUri: window.location.origin });
    
  }
}

function hasRole(userRole) {
  return user.value.role === userRole;
}

async function initKeycloak() {
  try {
    if (keycloak.authenticated) {
      var userRole = 'guest'
      if (keycloak.hasRealmRole("seller")) {
        userRole = 'seller'
      }else if (keycloak.hasRealmRole("customer")) {
        userRole = 'customer'
      }
      user.value = {
        name: keycloak.tokenParsed?.preferred_username || "Guest",
        isLoggedIn: true,
        role: userRole
      };
    } else {
      user.value.isLoggedIn = false;
      user.value.role = 'guest';
    }
  } catch (error) {
    console.error('Keycloak initialization failed:', error);
  }
}
onMounted(initKeycloak);

</script>

<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-buttons">
        <NavButton :disabled="!hasRole('seller')" to="/myProducts" label="My Products" />
        <NavButton :disabled="hasRole('seller')" to="/products" label="Products" />
        <NavButton :disabled="!hasRole('customer')" to="/orders" label="Orders" />
        <NavButton :disabled="hasRole('seller')" to="/cart" label="Cart" />
      </div>

      <div class="actions">
        <ThemeButton :toggleTheme="toggleTheme" :theme="theme"/>
        <User :user="user" @auth="handleAuth" @logout="handleAuth"/>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Navbar Styles */
.navbar {
  background-color: var(--background-color); 
  border-bottom: 1px solid var(--border-color); 
  padding: var(--spacing-small) 0; 
  transition: background-color 0.3s, border-color 0.3s; 
}

.container {
  display: flex;
  align-items: center;
  max-width: 1400px; 
  margin: 0 auto; 
  padding: 0 var(--spacing-medium); 
}

.nav-buttons {
  flex-grow: 1;
  display: flex;
  justify-content: center; 
  gap: var(--spacing-medium);
}
.actions {
  display: flex; /* Ensures items are aligned horizontally */
  align-items: center; /* Vertically aligns ThemeButton and User */
  justify-content: flex-end; /* Aligns items to the right */
  gap: var(--spacing-medium); /* Adds space between ThemeButton and User */
  flex-wrap: nowrap; /* Prevent wrapping in normal layouts */
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-buttons {
    justify-content: center;
    margin-bottom: var(--spacing-small);
  }
  .actions {
    flex-wrap: wrap; /* Allow wrapping for smaller screens */
    justify-content: center; /* Center-align on smaller screens */
    gap: var(--spacing-small); /* Reduce gap for smaller screens */
  }

}
</style>
