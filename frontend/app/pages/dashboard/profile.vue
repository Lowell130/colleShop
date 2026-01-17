<script setup>
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { ref, reactive, onMounted } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const useSameAddress = ref(false);

const form = reactive({
    full_name: '',
    email: '',
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
    if (user.value) {
        form.full_name = user.value.full_name || '';
        form.email = user.value.email || '';
        form.tax_code = user.value.tax_code || '';
        if (user.value.shipping_address) Object.assign(form.shipping_address, user.value.shipping_address);
        if (user.value.billing_address) {
            Object.assign(form.billing_address, user.value.billing_address);
            // Check if billing matches shipping to auto-check box?
            // For simplicity, we default to false unless user explicitly checks it, or could compare values.
            // Let's keep it simple: defaulting to false.
        }
    }
});

const saveProfile = async () => {
    loading.value = true;
    successMessage.value = '';
    errorMessage.value = '';

    try {
        const payload = { ...form };
        if (useSameAddress.value) {
            payload.billing_address = { ...form.shipping_address };
        }
        
        await authStore.updateProfile(payload);
        successMessage.value = 'Profilo aggiornato con successo!';
        setTimeout(() => successMessage.value = '', 3000);
    } catch (e) {
        errorMessage.value = 'Errore durante l\'aggiornamento del profilo.';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
  <div class="pb-20">
    <h1 class="text-3xl font-serif text-stone-900 mb-8">Il Mio Profilo</h1>

    <div v-if="successMessage" class="bg-green-100 text-green-800 p-4 rounded-sm mb-6 border border-green-200">
        {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="bg-red-100 text-red-800 p-4 rounded-sm mb-6 border border-red-200">
        {{ errorMessage }}
    </div>

    <form @submit.prevent="saveProfile" class="grid lg:grid-cols-2 gap-8">
        <!-- Personal Info -->
        <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 lg:col-span-2">
            <h2 class="text-xl font-serif text-stone-900 mb-6">Informazioni Personali</h2>
            <div class="grid md:grid-cols-2 gap-6">
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Nome Completo</label>
                     <input v-model="form.full_name" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 focus:ring-1 focus:ring-wine-900 outline-none transition-colors">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Email</label>
                     <input v-model="form.email" type="email" class="w-full border border-stone-300 p-3 rounded-sm bg-stone-50 cursor-not-allowed" disabled>
                </div>
                <div class="md:col-span-2">
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Codice Fiscale *</label>
                     <input v-model="form.tax_code" type="text" placeholder="CF obbligatorio per fatturazione" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 focus:ring-1 focus:ring-wine-900 outline-none transition-colors uppercase">
                </div>
            </div>
        </div>

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
                         <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Telefono</label>
                         <input v-model="form.shipping_address.phone" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                    </div>
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

        <div class="lg:col-span-2 flex justify-end">
             <button type="submit" :disabled="loading" class="bg-wine-900 text-white px-8 py-4 rounded-sm font-bold uppercase tracking-widest text-sm hover:bg-wine-800 transition-all shadow-xl disabled:opacity-50">
                {{ loading ? 'Salvataggio...' : 'Salva Modifiche' }}
            </button>
        </div>
    </form>
  </div>
</template>
