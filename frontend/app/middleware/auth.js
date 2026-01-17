
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';

export default defineNuxtRouteMiddleware((to, from) => {
    const authStore = useAuthStore();
    const { isAuthenticated } = storeToRefs(authStore);

    // If not authenticated and trying to access dashboard
    if (!isAuthenticated.value && to.path.startsWith('/dashboard')) {
        return navigateTo('/login');
    }

    // If authenticated and trying to access login
    if (isAuthenticated.value && to.path === '/login') {
        return navigateTo('/dashboard');
    }
});
