import { createRouter, createWebHistory } from 'vue-router';
import keycloak from '../auth/keycloak'; // Import Keycloak instance

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'default', // Default route for redirection based on roles
      beforeEnter: (to, from, next) => {
        if (!keycloak.authenticated) {
          next('/products');
        } else if (keycloak.hasRealmRole('seller')) {
          next('/myProducts');
        } else {
          next('/products');
        }
      },
    },
    {
      path: '/myProducts',
      name: 'myProducts',
      component: () => import('../views/MyProductsView.vue'),
      meta: { requiresAuth: true, roles: ['seller'] }, 
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue'),
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrdersView.vue'),
      meta: { requiresAuth: true, roles: ['customer']  }, 
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue'),
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
});

// Global Navigation Guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    
    if (!keycloak.authenticated) {
      keycloak
        .login({ redirectUri: window.location.href })
        .then(() => next())
        .catch((err) => {
          console.error('Keycloak login failed:', err);
          next(false);
        });
    } else if (to.meta.roles && !(hasRequiredRole(to.meta.roles))) {
      const targetUrl = to.fullPath;

      keycloak.logout({
        redirectUri: window.location.origin + targetUrl // Redirect after logout to the target page
      });
    
      
    } else {
      next(); 
    }
  } else {
    next(); 
  }
});

function hasRequiredRole(requiredRoles) {
  try {
    keycloak.updateToken(-1);
    return requiredRoles.some((role) => keycloak.hasRealmRole(role)); 
  } catch (err) {
    console.error('Failed to update token:', err);
    return false; 
  }
}

export default router;
