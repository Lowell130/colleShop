<script setup>
import { useRoute } from 'vue-router';
import { useOrdersStore } from '~/stores/orders';
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { ref, onMounted, computed } from 'vue';

definePageMeta({
    layout: 'dashboard',
    middleware: 'auth'
});

const route = useRoute();
const ordersStore = useOrdersStore();
const authStore = useAuthStore();
const { isAdmin } = storeToRefs(authStore);

const order = ref(null);
const loading = ref(true);
const error = ref(null);
const updating = ref(false);

onMounted(async () => {
    try {
        order.value = await ordersStore.fetchOrderById(route.params.id);
    } catch (e) {
        error.value = "Impossibile caricare l'ordine. Potrebbe non esistere o non hai i permessi.";
    } finally {
        loading.value = false;
    }
});

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', { 
        year: 'numeric', month: 'long', day: 'numeric', 
        hour: '2-digit', minute: '2-digit' 
    });
};

const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};

const updateStatus = async (event) => {
    const newStatus = event.target.value;
    if (!newStatus) return;
    
    updating.value = true;
    try {
        const updatedOrder = await ordersStore.updateOrderStatus(order.value._id, newStatus);
        order.value = updatedOrder;
    } catch (e) {
        alert("Errore durante l'aggiornamento dello stato");
    } finally {
        updating.value = false;
    }
};

const translateStatus = (status) => {
    switch (status) {
        case 'pending': return 'In elaborazione';
        case 'paid': return 'Pagato';
        case 'shipped': return 'Spedito';
        case 'cancelled': return 'Cancellato';
        default: return status;
    }
};
</script>

<template>
  <div class="pb-20">
    <!-- Back Link -->
    <div class="mb-6">
        <NuxtLink to="/dashboard/orders" class="text-stone-500 hover:text-wine-900 flex items-center gap-2 text-sm font-bold uppercase tracking-widest">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Torna agli Ordini
        </NuxtLink>
    </div>

    <!-- Loading/Error -->
    <div v-if="loading" class="text-center py-12">
         <span class="text-wine-900 font-bold animate-pulse">Caricamento dettagli ordine...</span>
    </div>
    <div v-if="error" class="bg-red-100 text-red-800 p-6 rounded-sm border border-red-200">
        {{ error }}
    </div>

    <!-- Order Content -->
    <div v-if="order" class="space-y-8 animate-fade-in-up">
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-stone-200 pb-6">
            <div>
                 <h1 class="text-3xl font-serif text-stone-900 mb-2">Ordine #{{ order._id.slice(-6) }}</h1>
                 <p class="text-stone-500 text-sm">Effettuato il {{ formatDate(order.created_at) }}</p>
                 <p v-if="order.customer_name" class="text-stone-500 text-sm mt-1">Cliente: <span class="text-stone-900 font-bold">{{ order.customer_name }}</span> ({{ order.customer_email }})</p>
                 <p v-if="order.customer_tax_code" class="text-stone-500 text-sm mt-1">C.F.: <span class="text-stone-900 font-bold uppercase">{{ order.customer_tax_code }}</span></p>
            </div>
            
            <div class="flex flex-col items-end gap-2">
                 <!-- Admin Controls -->
                 <div v-if="isAdmin" class="flex items-center gap-2 bg-stone-100 p-2 rounded-sm border border-stone-200">
                    <span class="text-xs font-bold uppercase tracking-widest text-stone-500">Stato:</span>
                    <select :value="order.status" @change="updateStatus" :disabled="updating" class="bg-white border text-sm border-stone-300 rounded-sm px-2 py-1 outline-none focus:border-wine-900 cursor-pointer">
                        <option value="pending">In elaborazione</option>
                        <option value="paid">Pagato</option>
                        <option value="shipped">Spedito</option>
                        <option value="cancelled">Cancellato</option>
                    </select>
                    <span v-if="updating" class="animate-spin h-4 w-4 border-2 border-wine-900 border-t-transparent rounded-full block"></span>
                 </div>
                 <!-- User View Status -->
                 <div v-else>
                     <span class="px-4 py-2 rounded-full text-sm font-bold uppercase tracking-widest bg-yellow-100 text-yellow-800" v-if="order.status === 'pending'">In elaborazione</span>
                     <span class="px-4 py-2 rounded-full text-sm font-bold uppercase tracking-widest bg-green-100 text-green-800" v-else-if="order.status === 'paid'">Pagato</span>
                     <span class="px-4 py-2 rounded-full text-sm font-bold uppercase tracking-widest bg-blue-100 text-blue-800" v-else-if="order.status === 'shipped'">Spedito</span>
                     <span class="px-4 py-2 rounded-full text-sm font-bold uppercase tracking-widest bg-red-100 text-red-800" v-else-if="order.status === 'cancelled'">Cancellato</span>
                 </div>
            </div>
        </div>

        <!-- Items Table -->
        <div class="bg-white rounded-sm shadow-sm border border-stone-100 overflow-hidden">
            <table class="w-full text-left">
                <thead class="bg-stone-50 text-xs font-bold uppercase tracking-widest text-stone-500">
                    <tr>
                        <th class="p-4">Prodotto</th>
                        <th class="p-4 text-center">Quantità</th>
                        <th class="p-4 text-right">Prezzo</th>
                        <th class="p-4 text-right">Totale</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-stone-100">
                    <tr v-for="item in order.items" :key="item.product_id" class="hover:bg-stone-50/50">
                        <td class="p-4 font-medium text-stone-900">{{ item.name }}</td>
                        <td class="p-4 text-center text-stone-600">{{ item.quantity }}</td>
                        <td class="p-4 text-right text-stone-600">{{ formatPrice(item.price) }}</td>
                        <td class="p-4 text-right font-bold text-wine-900">{{ formatPrice(item.price * item.quantity) }}</td>
                    </tr>
                </tbody>
                <tfoot class="bg-stone-50 border-t border-stone-100">
                    <tr>
                        <td colspan="3" class="p-4 text-right font-bold uppercase tracking-widest text-stone-600">Totale Ordine</td>
                        <td class="p-4 text-right text-xl font-serif text-wine-900 font-bold">{{ formatPrice(order.total_amount) }}</td>
                    </tr>
                </tfoot>
            </table>
        </div>

        <!-- Addresses -->
        <div class="grid md:grid-cols-2 gap-8">
            <!-- Shipping -->
            <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100">
                <h3 class="text-lg font-serif text-stone-900 mb-4 border-b border-stone-100 pb-2">Indirizzo di Spedizione</h3>
                <div v-if="order.shipping_address" class="text-stone-600 space-y-1">
                    <p class="font-bold text-stone-900">{{ order.customer_name }}</p>
                    <p>{{ order.shipping_address.street }}</p>
                    <p>{{ order.shipping_address.zip_code }} {{ order.shipping_address.city }} ({{ order.shipping_address.country }})</p>
                    <p class="text-sm mt-2 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                        {{ order.shipping_address.phone }}
                    </p>
                </div>
                <div v-else class="text-stone-400 italic">Nessun indirizzo specificato</div>
            </div>

            <!-- Billing -->
            <div class="bg-white p-6 rounded-sm shadow-sm border border-stone-100">
                <h3 class="text-lg font-serif text-stone-900 mb-4 border-b border-stone-100 pb-2">Dati Fatturazione</h3>
                <div v-if="order.billing_address" class="text-stone-600 space-y-1">
                    <p>{{ order.billing_address.street }}</p>
                    <p>{{ order.billing_address.zip_code }} {{ order.billing_address.city }} ({{ order.billing_address.country }})</p>
                    <p class="text-sm mt-2 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                        {{ order.billing_address.phone }}
                    </p>
                </div>
                <div v-else class="text-stone-400 italic">Stessi della spedizione</div>
            </div>
        </div>
    </div>
  </div>
</template>
