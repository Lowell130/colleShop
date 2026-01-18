<script setup>
import { useSettingsStore } from '~/stores/settings';
import { useAuthStore } from '~/stores/auth';
import { onMounted, reactive, ref } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const settingsStore = useSettingsStore();
const authStore = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const message = ref('');

const form = reactive({
    shipping_cost: 10,
    free_shipping_threshold: 100
});

onMounted(async () => {
    await settingsStore.fetchSettings();
    if (settingsStore.settings) {
        if (settingsStore.settings.shipping_cost !== undefined) form.shipping_cost = settingsStore.settings.shipping_cost;
        if (settingsStore.settings.free_shipping_threshold !== undefined) form.free_shipping_threshold = settingsStore.settings.free_shipping_threshold;
    }
    loading.value = false;
});

const save = async () => {
    saving.value = true;
    message.value = '';
    // We only send the fields we want to update.
    // The store likely sends the whole object or partial?
    // Let's check the store implementation later, but assuming we pass 'form' it might be partial.
    // Actually, settingsStore.updateSettings takes 'settings'. Check store logic.
    // If store just POSTs the payload, and backend handles partials (exclude_unset=True), we are good.
    const success = await settingsStore.updateSettings(form, authStore.token);
    if (success) {
        message.value = 'Configurazione spedizioni salvata!';
    } else {
        message.value = 'Errore durante il salvataggio.';
    }
    saving.value = false;
};
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-3xl font-serif text-stone-900 mb-8">Gestione Spedizioni</h1>
    
    <div v-if="loading" class="text-center py-10">Caricamento...</div>
    
    <form v-else @submit.prevent="save" class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 space-y-6">
        
        <div>
             <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2">Tariffe e Soglie</h2>
             <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                 <div>
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Costo Spedizione Standard (€)</label>
                    <input v-model.number="form.shipping_cost" type="number" step="0.01" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                 </div>
                 <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Soglia Spedizione Gratuita (€)</label>
                     <input v-model.number="form.free_shipping_threshold" type="number" step="0.01" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                     <p class="text-xs text-stone-400 mt-1">Se il totale dell'ordine supera questo importo, la spedizione è gratuita.</p>
                 </div>
             </div>
        </div>

        <div class="flex items-center gap-4 pt-4">
            <button type="submit" :disabled="saving" class="bg-wine-900 text-white px-6 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-colors disabled:opacity-50">
                {{ saving ? 'Salvataggio...' : 'Salva Configurazione' }}
            </button>
            <span v-if="message" :class="{'text-green-600': message.includes('salvata'), 'text-red-600': message.includes('Errore')}" class="text-sm font-bold animate-pulse">{{ message }}</span>
        </div>

    </form>
  </div>
</template>
