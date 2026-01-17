<script setup>
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { ref, onMounted } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const authStore = useAuthStore();
const { isAdmin, user } = storeToRefs(authStore);

const data = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
    try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/analytics/dashboard`, {
             headers: {
                'Authorization': `Bearer ${authStore.token}`
            }
        });
        if (!response.ok) throw new Error('Errore nel caricamento dati');
        data.value = await response.json();
    } catch (e) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
});

const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', { year: 'numeric', month: 'long', day: 'numeric' });
};
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif text-stone-900 mb-2">Panoramica</h1>
    <p class="text-stone-500 mb-8">Bentornato, <span class="font-bold text-wine-900">{{ user?.fullName }}</span></p>
    
    <!-- Loading/Error -->
    <div v-if="loading" class="py-12 text-center animate-pulse text-wine-900 font-bold">Caricamento dati...</div>
    <div v-else-if="error" class="bg-red-50 text-red-800 p-4 rounded-sm border border-red-200">{{ error }}</div>

    <div v-else>
        <!-- ADMIN DASHBOARD -->
        <div v-if="isAdmin" class="space-y-8 animate-fade-in-up">
             <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Fatturato Totale</h3>
                    <div class="text-3xl font-serif text-wine-900 font-bold mt-auto">{{ formatPrice(data.total_revenue) }}</div>
                </div>
                <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Totale Ordini</h3>
                    <div class="text-3xl font-serif text-stone-900 font-bold mt-auto">{{ data.total_orders }}</div>
                </div>
                <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Prodotti a Catalogo</h3>
                    <div class="text-3xl font-serif text-stone-900 font-bold mt-auto">{{ data.total_products }}</div>
                </div>
                 <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Utenti Registrati</h3>
                    <div class="text-3xl font-serif text-stone-900 font-bold mt-auto">{{ data.total_users }}</div>
                </div>
            </div>
            
            <!-- Recent Orders Table -->
             <div class="bg-white rounded-sm shadow-sm border border-stone-100 overflow-hidden">
                <div class="px-6 py-4 border-b border-stone-100 flex justify-between items-center bg-stone-50">
                    <h2 class="font-bold text-stone-800 uppercase text-xs tracking-widest">Ordini Recenti</h2>
                    <NuxtLink to="/dashboard/orders" class="text-xs text-wine-900 font-bold uppercase hover:underline">Vedi Tutti</NuxtLink>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead>
                            <tr class="text-stone-500 border-b border-stone-100">
                                <th class="px-6 py-3 font-medium">ID</th>
                                <th class="px-6 py-3 font-medium">Cliente</th>
                                <th class="px-6 py-3 font-medium">Data</th>
                                <th class="px-6 py-3 font-medium">Totale</th>
                                <th class="px-6 py-3 font-medium">Stato</th>
                                <th class="px-6 py-3 text-right">Azioni</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-stone-100">
                            <tr v-for="order in data.recent_orders" :key="order._id" class="hover:bg-stone-50/50">
                                <td class="px-6 py-3 text-stone-400 font-mono text-xs">#{{ order._id.slice(-6) }}</td>
                                <td class="px-6 py-3 font-medium text-stone-900">
                                    {{ order.customer_name || 'N/A' }}
                                    <div class="text-xs text-stone-400 font-normal">{{ order.customer_email }}</div>
                                </td>
                                <td class="px-6 py-3 text-stone-600">{{ formatDate(order.created_at) }}</td>
                                <td class="px-6 py-3 font-bold text-wine-900">{{ formatPrice(order.total_amount) }}</td>
                                <td class="px-6 py-3">
                                     <span class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-yellow-100 text-yellow-800" v-if="order.status === 'pending'">In elaborazione</span>
                                     <span class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-green-100 text-green-800" v-else-if="order.status === 'paid'">Pagato</span>
                                     <span class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-blue-100 text-blue-800" v-else-if="order.status === 'shipped'">Spedito</span>
                                      <span class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-red-100 text-red-800" v-else-if="order.status === 'cancelled'">Cancellato</span>
                                </td>
                                <td class="px-6 py-3 text-right">
                                    <NuxtLink :to="`/dashboard/orders/${order._id}`" class="text-stone-400 hover:text-wine-900">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                                    </NuxtLink>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                     <div v-if="data.recent_orders.length === 0" class="p-8 text-center text-stone-500 italic">Nessun ordine recente.</div>
                </div>
            </div>
        </div>

        <!-- USER DASHBOARD -->
        <div v-else class="space-y-8 animate-fade-in-up">
            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col justify-between h-32">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">I Miei Ordini</h3>
                    <div class="text-3xl font-serif text-stone-900">{{ data.total_orders }}</div>
                </div>
                <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col justify-between h-32">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Spesa Totale</h3>
                    <div class="text-3xl font-serif text-stone-900">{{ formatPrice(data.total_spent) }}</div>
                </div>
                 <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100 flex flex-col justify-between h-32 relative overflow-hidden group hover:border-wine-200 transition-colors cursor-pointer" @click="$router.push('/shop')">
                    <div class="absolute -right-4 -bottom-4 opacity-10 group-hover:opacity-20 transition-opacity">
                         <svg xmlns="http://www.w3.org/2000/svg" class="h-32 w-32" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                    </div>
                    <h3 class="text-xs font-bold uppercase tracking-widest text-wine-900 mb-2">Nuovo Ordine</h3>
                    <div class="text-sm text-stone-600 mt-auto flex items-center gap-1">
                        Vai allo Shop 
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                    </div>
                </div>
            </div>

            <!-- Last Order / Call to Action -->
            <div v-if="data.last_order" class="bg-white rounded-sm shadow-sm border border-stone-100 p-8 flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                     <span class="text-xs font-bold uppercase tracking-widest text-stone-400 block mb-2">Ultimo Ordine</span>
                     <h2 class="text-xl font-serif text-stone-900 mb-1">Ordine #{{ data.last_order._id.slice(-6) }}</h2>
                     <p class="text-stone-500 text-sm">Del {{ formatDate(data.last_order.created_at) }} • <span class="text-stone-900 font-bold">{{ formatPrice(data.last_order.total_amount) }}</span></p>
                </div>
                <NuxtLink :to="`/dashboard/orders/${data.last_order._id}`" class="bg-stone-900 text-white px-6 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-stone-800 transition-colors">
                    Vedi Dettagli
                </NuxtLink>
            </div>
        </div>
    </div>

  </div>
</template>
