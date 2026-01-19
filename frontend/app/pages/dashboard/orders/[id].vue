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

import { useSettingsStore } from '~/stores/settings';
const settingsStore = useSettingsStore();

const itemsTotal = computed(() => {
    if (!order.value) return 0;
    return order.value.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

const shippingCost = computed(() => {
    if (!order.value) return 0;
    // Difference between Total Amount and Sum of Items
    const cost = order.value.total_amount - itemsTotal.value;
    return Math.max(0, cost); // Prevent negative due to float precision
});

const vatRate = computed(() => settingsStore.settings?.vat_rate ?? 22);

const vatAmount = computed(() => {
    if (!itemsTotal.value) return 0;
    // Items Price is Gross (Net + VAT).
    // Gross = Net * (1 + rate/100)
    // Net = Gross / (1 + rate/100)
    // VAT = Gross - Net
    return itemsTotal.value - (itemsTotal.value / (1 + vatRate.value / 100));
});

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

const showTrackingModal = ref(false);
const trackingForm = ref({ courier: '', number: '' });
const pendingStatus = ref(null);

const updateStatus = async (event) => {
    const newStatus = event.target.value;
    if (!newStatus) return;

    // Check if status is shipped to trigger modal
    if (newStatus === 'shipped') {
        pendingStatus.value = newStatus;
        showTrackingModal.value = true;
        // Don't update yet
        return;
    }
    
    // Direct update for other statuses
    await performUpdate(newStatus);
};

const confirmTracking = async () => {
    showTrackingModal.value = false;
    await performUpdate('shipped', trackingForm.value.number, trackingForm.value.courier);
    // Reset form
    trackingForm.value = { courier: '', number: '' };
};

const cancelTracking = () => {
    showTrackingModal.value = false;
    pendingStatus.value = null;
    // Force UI refresh or reset select? Ideally select binds to order.status so it should revert automatically if we didn't change it.
    // However, the event changed the UI select value. We might need to force update key or similar, but since we bind :value="order.status", Vue should revert it on next tick if order.status didn't change.
};

const performUpdate = async (status, tracking = null, courier = null) => {
    updating.value = true;
    try {
        const updatedOrder = await ordersStore.updateOrderStatus(order.value._id, status, tracking, courier);
        order.value = updatedOrder;
    } catch (e) {
        alert("Errore durante l'aggiornamento dello stato");
    } finally {
        updating.value = false;
    }
}

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
                        <td colspan="3" class="p-4 text-right uppercase tracking-widest text-xs text-stone-500">Spedizione</td>
                        <td class="p-4 text-right font-medium text-stone-600">{{ formatPrice(shippingCost) }}</td>
                    </tr>
                    <tr>
                         <td colspan="3" class="p-4 text-right font-bold uppercase tracking-widest text-stone-600">Totale Ordine</td>
                         <td class="p-4 text-right text-xl font-serif text-wine-900 font-bold">{{ formatPrice(order.total_amount) }}</td>
                    </tr>
                    <tr>
                        <td colspan="4" class="p-2 text-right text-xs text-stone-400 italic">
                            (Di cui IVA {{ vatRate }}%: {{ formatPrice(vatAmount) }})
                        </td>
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
                    <p>{{ order.shipping_address.zip_code }} {{ order.shipping_address.city }} {{ order.shipping_address.province ? '(' + order.shipping_address.province + ')' : '' }} - {{ order.shipping_address.country }}</p>
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
                    <p>{{ order.billing_address.zip_code }} {{ order.billing_address.city }} {{ order.billing_address.province ? '(' + order.billing_address.province + ')' : '' }} - {{ order.billing_address.country }}</p>
                    <p class="text-sm mt-2 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
                        {{ order.billing_address.phone }}
                    </p>
                </div>
                <div v-else class="text-stone-400 italic">Stessi della spedizione</div>
            </div>
            
             <!-- Tracking Info Display -->
            <div v-if="order.tracking_number" class="md:col-span-2 bg-stone-50 p-6 rounded-sm border border-stone-200">
                <h3 class="text-lg font-serif text-stone-900 mb-4 border-b border-stone-200 pb-2 flex items-center gap-2">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-wine-900" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" /></svg>
                    Spedizione
                </h3>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <span class="block text-xs font-bold uppercase tracking-widest text-stone-500">Corriere</span>
                        <span class="text-lg font-bold text-stone-800">{{ order.courier_name || 'N/D' }}</span>
                    </div>
                    <div>
                        <span class="block text-xs font-bold uppercase tracking-widest text-stone-500">Tracking Number</span>
                        <span class="text-lg font-mono text-stone-800 bg-white px-2 py-1 rounded border border-stone-200 inline-block">{{ order.tracking_number }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tracking Modal -->
    <Teleport to="body">
        <div v-if="showTrackingModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
            <div class="bg-white rounded-sm shadow-2xl p-8 max-w-md w-full animate-fade-in-up">
                <h3 class="text-2xl font-serif text-wine-900 mb-4">Inserisci Tracking</h3>
                <p class="text-stone-600 mb-6 text-sm">Hai impostato l'ordine come <strong>Spedito</strong>. Inserisci i dettagli per il cliente.</p>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-1">Corriere</label>
                        <input v-model="trackingForm.courier" type="text" class="w-full border border-stone-300 p-2 rounded-sm focus:border-wine-900 outline-none" placeholder="Es. Bartolini, DHL...">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-1">Tracking Number</label>
                        <input v-model="trackingForm.number" type="text" class="w-full border border-stone-300 p-2 rounded-sm focus:border-wine-900 outline-none" placeholder="Codice tracciamento">
                    </div>
                </div>

                <div class="flex justify-end gap-3 mt-8">
                    <button @click="cancelTracking" class="px-4 py-2 text-stone-500 hover:text-stone-800 font-bold uppercase tracking-widest text-xs">Annulla</button>
                    <button @click="confirmTracking" class="bg-wine-900 text-white px-6 py-2 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-colors">Conferma & Invia</button>
                </div>
            </div>
        </div>
    </Teleport>

  </div>
</template>
