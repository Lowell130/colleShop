<script setup>
import { useSettingsStore } from '~/stores/settings';
import { useAuthStore } from '~/stores/auth';
import { onMounted, reactive, ref } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth' // And we should check admin role
});

const settingsStore = useSettingsStore();
const authStore = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const message = ref('');

const form = reactive({
    address: '',
    email: '',
    phone: '',
    hours_weekdays: '',
    hours_saturday: '',
    hours_sunday: '',
    google_maps_url: '',
    booking_email: '',
    facebook_url: '',
    instagram_url: '',
    privacy_text: '',
    terms_text: ''
});

onMounted(async () => {
    await settingsStore.fetchSettings();
    if (settingsStore.settings) {
        Object.assign(form, settingsStore.settings);
    }
    loading.value = false;
});

const save = async () => {
    saving.value = true;
    message.value = '';
    const success = await settingsStore.updateSettings(form, authStore.token);
    if (success) {
        message.value = 'Impostazioni salvate con successo!';
    } else {
        message.value = 'Errore durante il salvataggio.';
    }
    saving.value = false;
};
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-3xl font-serif text-stone-900 mb-8">Impostazioni Sito</h1>
    
    <div v-if="loading" class="text-center py-10">Caricamento...</div>
    
    <form v-else @submit.prevent="save" class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 space-y-6">
        
        <!-- Contact Info -->
        <div>
            <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2">I Nostri Recapiti</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="md:col-span-2">
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Indirizzo Fisico</label>
                    <input v-model="form.address" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Email Pubblica</label>
                     <input v-model="form.email" type="email" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Telefono</label>
                     <input v-model="form.phone" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
            </div>
        </div>

        <!-- Opening Hours -->
        <div>
            <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2 mt-4">Orari Cantina</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Lun - Ven</label>
                    <input v-model="form.hours_weekdays" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Sabato</label>
                     <input v-model="form.hours_saturday" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Domenica</label>
                     <input v-model="form.hours_sunday" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
            </div>
        </div>
        
        <!-- Other Config -->
         <div>
            <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2 mt-4">Configurazioni Extra</h2>
            <div class="space-y-4">
                <div>
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">URL Google Maps (Embed o Link)</label>
                    <input v-model="form.google_maps_url" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none text-sm font-mono">
                    <p class="text-xs text-stone-400 mt-1">Inserisci l'URL completo per il link.</p>
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Email per Prenotazioni (Bottone)</label>
                     <input v-model="form.booking_email" type="email" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none">
                </div>
            </div>
        </div>

        <!-- Social Media -->
        <div>
            <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2 mt-4">Social Media</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Facebook URL</label>
                    <input v-model="form.facebook_url" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none text-sm placeholder-stone-300" placeholder="https://facebook.com/...">
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Instagram URL</label>
                     <input v-model="form.instagram_url" type="text" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none text-sm placeholder-stone-300" placeholder="https://instagram.com/...">
                </div>
            </div>
        </div>

        <!-- Legal -->
        <div>
            <h2 class="text-lg font-bold text-stone-800 mb-4 border-b pb-2 mt-4">Note Legali (HTML/Testo)</h2>
            <div class="space-y-6">
                <div>
                    <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Privacy Policy</label>
                    <textarea v-model="form.privacy_text" rows="10" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none text-sm font-mono"></textarea>
                </div>
                <div>
                     <label class="block text-stone-500 text-xs font-bold uppercase tracking-widest mb-2">Termini & Condizioni</label>
                     <textarea v-model="form.terms_text" rows="10" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none text-sm font-mono"></textarea>
                </div>
            </div>
        </div>


        <!-- Action -->
        <div class="flex items-center gap-4 pt-4">
            <button type="submit" :disabled="saving" class="bg-wine-900 text-white px-6 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-colors disabled:opacity-50">
                {{ saving ? 'Salvataggio...' : 'Salva Modifiche' }}
            </button>
            <span v-if="message" :class="{'text-green-600': message.includes('successo'), 'text-red-600': message.includes('Errore')}" class="text-sm font-bold animate-pulse">{{ message }}</span>
        </div>

    </form>
  </div>
</template>
