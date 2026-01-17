<script setup>
import { useCartStore } from '~/stores/cart';
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { ref, reactive, onMounted } from 'vue';

definePageMeta({
    middleware: 'auth'
});

const cartStore = useCartStore();
const authStore = useAuthStore();
const router = useRouter();
const { items, totalPrice } = storeToRefs(cartStore);
const { user } = storeToRefs(authStore);

const processing = ref(false);
const error = ref(null);
const useSameAddress = ref(false);

const form = reactive({
    tax_code: '',
    shipping_address: {
        street: '',
        city: '',
        zip_code: '',
        country: '',
        phone: ''
    },
    billing_address: {
        street: '',
        city: '',
        zip_code: '',
        country: '',
        phone: ''
    }
});

onMounted(() => {
    // Restore from session storage if exists (came back from login)
    const storedForm = sessionStorage.getItem('checkout_form');
    if (storedForm) {
        try {
            Object.assign(form, JSON.parse(storedForm));
            const sameAddress = sessionStorage.getItem('checkout_same_address');
            if (sameAddress) useSameAddress.value = sameAddress === 'true';
            
            // Clear storage
            sessionStorage.removeItem('checkout_form');
            sessionStorage.removeItem('checkout_same_address');
        } catch (e) {
            console.error("Failed to restore checkout form", e);
        }
    } else if (user.value) {
        // Normal profile pre-fill
        form.tax_code = user.value.tax_code || '';
        if (user.value.shipping_address) Object.assign(form.shipping_address, user.value.shipping_address);
        if (user.value.billing_address) {
            Object.assign(form.billing_address, user.value.billing_address);
        }
    }
});

const handlePayment = async () => {
    processing.value = true;
    error.value = null;
    try {
        const payload = { ...form };
        if (useSameAddress.value) {
            payload.billing_address = { ...form.shipping_address };
        }
        // Basic validation
        if (!payload.shipping_address.street || !payload.shipping_address.city || !payload.shipping_address.zip_code) {
             throw new Error("L'indirizzo di spedizione è incompleto.");
        }
        if (!payload.tax_code) {
             throw new Error("Inserisci il Codice Fiscale.");
        }

        await cartStore.checkout(payload);
        // Redirect to user orders
        router.push('/dashboard/orders');
    } catch (err) {
        if (err.message.includes("Devi effettuare il login")) {
            // Save form state
            sessionStorage.setItem('checkout_form', JSON.stringify(form));
            sessionStorage.setItem('checkout_same_address', useSameAddress.value);
            // Redirect to login with return back
            router.push(`/login?redirect=${encodeURIComponent('/checkout')}`);
        } else {
            error.value = err.message;
        }
    } finally {
        processing.value = false;
    }
};

const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div class="pt-32 pb-20 px-8 bg-stone-50 min-h-screen">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-serif text-wine-900 mb-8">Checkout</h1>

        <div v-if="items.length > 0" class="grid lg:grid-cols-3 gap-12">
            
            <!-- Forms Column -->
            <div class="lg:col-span-2 space-y-8">
                 <!-- Shipping Address -->
                <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100">
                    <h2 class="text-xl font-serif text-stone-900 mb-6 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-wine-900" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" /></svg>
                        Indirizzo di Spedizione
                    </h2>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Via e Numero</label>
                            <input v-model="form.shipping_address.street" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Città</label>
                                <input v-model="form.shipping_address.city" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">CAP</label>
                                <input v-model="form.shipping_address.zip_code" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Paese</label>
                                <input v-model="form.shipping_address.country" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Paese</label>
                                <input v-model="form.shipping_address.country" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Telefono</label>
                                <input v-model="form.shipping_address.phone" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                        </div>
                         <!-- Tax Code -->
                        <div>
                             <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Codice Fiscale *</label>
                             <input v-model="form.tax_code" type="text" placeholder="CF per fatturazione" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none uppercase">
                        </div>
                    </div>
                </div>

                <!-- Billing Address -->
                <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                        <h2 class="text-xl font-serif text-stone-900 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-wine-900" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                            Dati di Fatturazione
                        </h2>
                        
                        <label class="flex items-center gap-2 cursor-pointer select-none">
                            <input type="checkbox" v-model="useSameAddress" class="form-checkbox h-4 w-4 text-wine-900 rounded border-stone-300 focus:ring-wine-900">
                            <span class="text-sm text-stone-600">Usa Indirizzo di Spedizione</span>
                        </label>
                    </div>

                    <div v-if="!useSameAddress" class="space-y-4 animate-fade-in-down">
                        <div>
                            <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Via e Numero</label>
                            <input v-model="form.billing_address.street" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Città</label>
                                <input v-model="form.billing_address.city" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">CAP</label>
                                <input v-model="form.billing_address.zip_code" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Paese</label>
                                <input v-model="form.billing_address.country" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                            <div>
                                <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Telefono</label>
                                <input v-model="form.billing_address.phone" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-stone-500 text-sm italic py-4">
                        I dati di fatturazione coincideranno con l'indirizzo di spedizione.
                    </div>
                </div>
            </div>

            <!-- Summary & Payment -->
            <div class="space-y-8">
                <!-- Order Summary -->
                <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100">
                    <h2 class="text-xl font-serif text-stone-900 mb-6">Riepilogo Ordine</h2>
                    <div class="space-y-4 mb-6">
                        <div v-for="item in items" :key="item.id" class="flex justify-between items-center text-sm">
                            <div class="flex items-center gap-3">
                                <span class="font-bold text-wine-900">{{ item.quantity }}x</span>
                                <span class="text-stone-700">{{ item.name }}</span>
                            </div>
                            <span class="font-medium text-stone-900">{{ formatPrice(item.price * item.quantity) }}</span>
                        </div>
                    </div>
                    <div class="border-t border-stone-100 pt-6 flex justify-between items-center text-lg font-serif font-bold text-wine-900">
                        <span>Totale</span>
                        <span>{{ formatPrice(totalPrice) }}</span>
                    </div>
                </div>

                <!-- Payment Simulation -->
                 <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 sticky top-32">
                    <h2 class="text-xl font-serif text-stone-900 mb-6">Pagamento</h2>
                    <p class="text-stone-500 text-sm mb-6">
                        Stiamo predisponendo il pagamento sicuro con Stripe. <br>
                        Cliccando "Paga Ora" simulerai una transazione riuscita e confermerai i dati inseriti.
                    </p>

                    <div v-if="error" class="bg-red-50 text-red-800 p-4 rounded-sm text-sm mb-6">
                        {{ error }}
                    </div>

                    <button @click="handlePayment" :disabled="processing" class="w-full bg-wine-900 text-white py-4 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2">
                        <svg v-if="processing" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span v-else>Paga Ora {{ formatPrice(totalPrice) }}</span>
                    </button>

                    <div class="mt-4 flex items-center justify-center gap-2 text-stone-400 text-xs">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                        <span>Pagamento criptato SSL</span>
                    </div>
                 </div>
            </div>
        </div>
        <div v-else class="text-center py-20">
            <p class="text-xl text-stone-500 mb-6">Il tuo carrello è vuoto.</p>
            <NuxtLink to="/shop" class="inline-block bg-wine-900 text-white px-8 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all">
                Torna allo Shop
            </NuxtLink>
        </div>
    </div>
  </div>
</template>
