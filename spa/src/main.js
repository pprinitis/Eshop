import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import keycloak from './auth/keycloak'
import { assignRoleToUser } from './auth/assignUserRole';

import 'primeicons/primeicons.css';


const app = createApp(App)
keycloak.onAuthSuccess = async () => {
  // Called when the user is successfully authenticated
  try {
    const username = keycloak.tokenParsed?.preferred_username;
    const userRole = keycloak.tokenParsed?.user_role; 
    if (username && userRole) {
      const result = await assignRoleToUser(username, userRole);   
      await keycloak.updateToken(-1); // Refresh the token if needed
    }else{
      console.warn("Missing username or user role in token.");
    }
  } catch (err) {
    console.error('Error assigning role:', err);
  }
};
keycloak
  .init({ onLoad: 'check-sso' }) 
  .then((authenticated) => {
    app.config.globalProperties.$keycloak = keycloak;
    app.use(router)

    app.mount("#app");
  })
  .catch((err) => {
    console.error("Failed to initialize Keycloak", err);
  });