<script setup>
import { useOrdersStore } from '~/stores/orders';
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { onMounted, computed } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const ordersStore = useOrdersStore();
const authStore = useAuthStore();
const { orders, loading } = storeToRefs(ordersStore);
const { isAdmin } = storeToRefs(authStore);

onMounted(() => {
    if (isAdmin.value) {
        ordersStore.fetchAllOrders();
    } else {
        ordersStore.fetchMyOrders();
    }
});

const pageTitle = computed(() => isAdmin.value ? 'Gestione Ordini' : 'I Miei Ordini');

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
};

const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif text-stone-900 mb-8">{{ pageTitle }}</h1>

    <div v-if="loading" class="text-center py-12">
         <span class="text-wine-900 font-bold animate-pulse">Caricamento ordini...</span>
    </div>

    <div v-else-if="orders.length === 0" class="bg-white p-12 rounded-sm shadow-sm border border-stone-100 text-center">
        <p class="text-stone-500 mb-6">Nessun ordine trovato.</p>
        <NuxtLink v-if="!isAdmin" to="/shop" class="text-wine-900 font-bold uppercase tracking-widest text-xs hover:underline">
            Inizia lo Shopping
        </NuxtLink>
    </div>

    <div v-else class="space-y-6">
        <div v-for="order in orders" :key="order._id" class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 hover:shadow-md transition-shadow">
            <div class="flex flex-wrap justify-between items-start gap-4 mb-4">
                <div>
                    <span class="text-xs font-bold uppercase tracking-widest text-stone-400 block mb-1">Ordine #{{ order._id.slice(-6) }}</span>
                    <span class="text-stone-900 font-medium block">{{ formatDate(order.created_at) }}</span>
                    <span v-if="isAdmin && order.customer_name" class="text-sm text-stone-500 mt-1 block">Cliente: {{ order.customer_name }}</span>
                </div>
                <div class="text-right">
                    <span class="text-xs font-bold uppercase tracking-widest text-stone-400 block mb-1">Totale</span>
                    <span class="text-xl font-serif text-wine-900">{{ formatPrice(order.total_amount) }}</span>
                </div>
                <div class="flex flex-col items-end gap-2">
                     <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest bg-yellow-100 text-yellow-800" v-if="order.status === 'pending'">In elaborazione</span>
                     <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest bg-green-100 text-green-800" v-else-if="order.status === 'paid'">Pagato</span>
                     <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest bg-blue-100 text-blue-800" v-else-if="order.status === 'shipped'">Spedito</span>
                     <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest bg-red-100 text-red-800" v-else-if="order.status === 'cancelled'">Cancellato</span>
                     
                     <NuxtLink :to="`/dashboard/orders/${order._id}`" class="text-xs text-stone-500 hover:text-wine-900 underline">Vedi Dettagli</NuxtLink>
                </div>
            </div>

            <div class="space-y-3">
                <div v-for="item in order.items" :key="item.product_id" class="flex justify-between text-sm">
                    <div class="flex items-center gap-2">
                        <span class="font-bold text-wine-900">{{ item.quantity }}x</span>
                        <span class="text-stone-700">{{ item.name }}</span>
                    </div>
                    <span class="text-stone-500">{{ formatPrice(item.price * item.quantity) }}</span>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
