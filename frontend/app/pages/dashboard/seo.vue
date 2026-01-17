<script setup>
import { useSettingsStore } from '~/stores/settings';
import { useAuthStore } from '~/stores/auth';
import { ref, onMounted, computed } from 'vue';

definePageMeta({
    layout: 'dashboard',
    middleware: 'auth'
});

const settingsStore = useSettingsStore();
const authStore = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const showSuccess = ref(false);

const form = ref({
    seo_title: '',
    seo_description: '',
    seo_keywords: '',
    seo_image_url: ''
});

onMounted(async () => {
    if (!settingsStore.settings) {
        await settingsStore.fetchSettings();
    }
    if (settingsStore.settings) {
        form.value = {
            seo_title: settingsStore.settings.seo_title || '',
            seo_description: settingsStore.settings.seo_description || '',
            seo_keywords: settingsStore.settings.seo_keywords || '',
            seo_image_url: settingsStore.settings.seo_image_url || ''
        };
    }
    loading.value = false;
});

const saveSettings = async () => {
    saving.value = true;
    showSuccess.value = false;
    
    // We send only the updated fields, merged with existing settings logic in backend? 
    // Actually the update endpoint expects a SettingsUpdate model, so we should probably send all fields or rely on backend to partial update?
    // The store's updateSettings sends whatever we pass. The backend Pydantic model has defaults. 
    // Ideally we should merge with existing settings to avoid overwriting other fields with defaults if the API replaces the whole document.
    // Let's assume we need to send the full object or the store handles it.
    // Actually, looking at settings.py, it's a PUT. We should send the full object + updates.
    
    const updatedSettings = { ...settingsStore.settings, ...form.value };

    const success = await settingsStore.updateSettings(updatedSettings, authStore.token);
    
    if (success) {
        showSuccess.value = true;
        setTimeout(() => showSuccess.value = false, 3000);
    }
    saving.value = false;
};
</script>

<template>
  <div class="max-w-4xl">
    <div class="mb-8">
        <h1 class="text-3xl font-serif text-stone-900 mb-2">SEO & Metadati</h1>
        <p class="text-stone-600">Gestisci come il tuo sito appare su Google e sui Social Network.</p>
    </div>

    <div v-if="loading" class="py-12 text-center text-stone-500 animate-pulse">
        Caricamento impostazioni...
    </div>

    <div v-else class="grid lg:grid-cols-2 gap-8">
        <!-- Form -->
        <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 h-fit">
            <form @submit.prevent="saveSettings" class="space-y-6">
                
                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Titolo Sito (Meta Title)</label>
                    <input v-model="form.seo_title" type="text" class="w-full border-b border-stone-300 py-2 focus:border-wine-900 outline-none transition-colors" placeholder="Es. Il Colle Tinto - Vini Molisani">
                    <p class="text-xs text-stone-400 mt-1">Titolo principale che appare nella scheda del browser e su Google.</p>
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Descrizione (Meta Description)</label>
                    <textarea v-model="form.seo_description" rows="3" class="w-full border border-stone-300 p-3 rounded-sm focus:border-wine-900 outline-none transition-colors" placeholder="Breve descrizione del sito..."></textarea>
                    <p class="text-xs text-stone-400 mt-1">Consigliato: 150-160 caratteri.</p>
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Keywords</label>
                    <input v-model="form.seo_keywords" type="text" class="w-full border-b border-stone-300 py-2 focus:border-wine-900 outline-none transition-colors" placeholder="vino, molise, tintilia, ...">
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Social Image URL (OG:Image)</label>
                    <input v-model="form.seo_image_url" type="text" class="w-full border-b border-stone-300 py-2 focus:border-wine-900 outline-none transition-colors" placeholder="https://...">
                    <p class="text-xs text-stone-400 mt-1">Immagine mostrata quando condividi il link su Facebook/WhatsApp.</p>
                </div>

                <div class="pt-6">
                    <button type="submit" :disabled="saving" class="bg-wine-900 text-white px-8 py-3 rounded-sm font-bold uppercase tracking-widest hover:bg-wine-800 transition-colors disabled:opacity-50 w-full flex justify-center items-center gap-2">
                        <span v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                        {{ saving ? 'Salvataggio...' : 'Salva Modifiche' }}
                    </button>
                </div>

                <div v-if="showSuccess" class="bg-green-50 text-green-800 p-4 rounded-sm text-center font-medium animate-fade-in-up">
                    Impostazioni SEO aggiornate con successo!
                </div>
            </form>
        </div>

        <!-- Preview -->
        <div class="space-y-6">
            <h3 class="font-bold text-stone-900 uppercase tracking-widest text-sm">Anteprima Ricerca Google</h3>
            
            <div class="bg-white p-6 rounded-lg shadow-sm border border-stone-200 font-sans">
                <div class="flex items-center gap-2 mb-1">
                    <div class="bg-stone-100 rounded-full w-7 h-7 flex items-center justify-center text-xs overflow-hidden">
                        <img src="/favicon.ico" class="w-4 h-4 opacity-50" onerror="this.style.display='none'" />
                    </div>
                    <div class="flex flex-col leading-tight">
                        <span class="text-stone-800 text-sm">ilcolletinto.it</span>
                        <span class="text-stone-500 text-xs">https://www.ilcolletinto.it</span>
                    </div>
                    <div class="ml-auto text-stone-400">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" /></svg>
                    </div>
                </div>
                <h4 class="text-[#1a0dab] text-xl cursor-pointer hover:underline truncate">{{ form.seo_title || 'Titolo Del Sito' }}</h4>
                <p class="text-stone-600 text-sm mt-1 line-clamp-2">
                    {{ form.seo_description || 'Qui apparirà la descrizione del tuo sito web così come verrà mostrata nei risultati di ricerca di Google.' }}
                </p>
            </div>

            <h3 class="font-bold text-stone-900 uppercase tracking-widest text-sm mt-8">Anteprima Social Card</h3>
             <div class="bg-white rounded-lg shadow-sm border border-stone-200 overflow-hidden max-w-sm mx-auto lg:mx-0">
                <div class="h-48 bg-stone-100 flex items-center justify-center overflow-hidden">
                    <img v-if="form.seo_image_url" :src="form.seo_image_url" class="w-full h-full object-cover" />
                    <span v-else class="text-stone-400 text-sm italic">Nessuna immagine</span>
                </div>
                <div class="p-4 bg-stone-50 border-t border-stone-100">
                    <div class="uppercase text-xs text-stone-500 mb-1">ILCOLLETINTO.IT</div>
                    <div class="font-bold text-stone-900 mb-1 leading-tight">{{ form.seo_title }}</div>
                    <div class="text-sm text-stone-600 line-clamp-1">{{ form.seo_description }}</div>
                </div>
             </div>

        </div>
    </div>
  </div>
</template>
