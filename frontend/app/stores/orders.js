import { defineStore } from 'pinia';
import { useAuthStore } from './auth';

export const useOrdersStore = defineStore('orders', {
    state: () => ({
        orders: [],
        loading: false,
        error: null
    }),
    actions: {
        async fetchMyOrders() {
            this.loading = true;
            this.error = null;
            const authStore = useAuthStore();
            try {
                const response = await fetch('http://localhost:8000/orders/mine', {
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                });
                if (!response.ok) throw new Error('Failed to fetch orders');
                this.orders = await response.json();
            } catch (err) {
                this.error = err.message;
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async fetchAllOrders() {
            this.loading = true;
            this.error = null;
            const authStore = useAuthStore();
            try {
                const response = await fetch('http://localhost:8000/orders/', {
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                });
                if (!response.ok) throw new Error('Failed to fetch orders');
                this.orders = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        async fetchOrderById(id) {
            const authStore = useAuthStore();
            try {
                const response = await fetch(`http://localhost:8000/orders/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                });
                if (!response.ok) throw new Error('Failed to fetch order');
                return await response.json();
            } catch (e) {
                console.error(e);
                throw e;
            }
        },
        async updateOrderStatus(id, status) {
            const authStore = useAuthStore();
            try {
                const response = await fetch(`http://localhost:8000/orders/${id}/status`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authStore.token}`
                    },
                    body: JSON.stringify({ status })
                });
                if (!response.ok) throw new Error('Failed to update status');
                return await response.json();
            } catch (e) {
                throw e;
            }
        }
    }
});
