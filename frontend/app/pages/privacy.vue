<script setup>
import { useSettingsStore } from '~/stores/settings';
import { onMounted, computed } from 'vue';

const settingsStore = useSettingsStore();

onMounted(() => {
    if (!settingsStore.settings) {
        settingsStore.fetchSettings();
    }
});

const s = computed(() => settingsStore.settings || {});
</script>

<template>
  <div class="pt-32 pb-20 px-8 bg-stone-50 min-h-screen">
    <div class="max-w-4xl mx-auto bg-white p-12 rounded-sm shadow-xl border border-stone-100">
        <h1 class="text-4xl font-serif text-wine-900 mb-8">Privacy Policy</h1>
        
        <div v-if="s.privacy_text" class="prose prose-stone max-w-none text-stone-600 leading-relaxed whitespace-pre-wrap" v-html="s.privacy_text"></div>
        <div v-else class="text-stone-400 italic">
            Nessuna privacy policy definita.
        </div>
    </div>
  </div>
</template>
