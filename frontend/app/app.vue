<script setup>
import { useSettingsStore } from '~/stores/settings';
import { useAuthStore } from '~/stores/auth';
import { useCartStore } from '~/stores/cart';
import { computed, watchEffect, onMounted } from 'vue';

const authStore = useAuthStore();
const cartStore = useCartStore();
const settingsStore = useSettingsStore();

// Initialize stores
// Auth and Settings can start early
authStore.initializeAuth();
settingsStore.fetchSettings();

// Cart relies on LocalStorage, best to init on mount to ensure client env
onMounted(() => {
    cartStore.initializeCart();
});

useHead({
  title: computed(() => settingsStore.settings?.seo_title || 'Il Colle Tinto'),
  meta: [
    { name: 'description', content: computed(() => settingsStore.settings?.seo_description || 'Vini d\'eccellenza dal Molise.') },
    { name: 'keywords', content: computed(() => settingsStore.settings?.seo_keywords || 'vino, molise, tintilia') },
    // Open Graph
    { property: 'og:title', content: computed(() => settingsStore.settings?.seo_title || 'Il Colle Tinto') },
    { property: 'og:description', content: computed(() => settingsStore.settings?.seo_description || 'Vini d\'eccellenza dal Molise.') },
    { property: 'og:image', content: computed(() => settingsStore.settings?.seo_image_url || '') },
    { property: 'og:type', content: 'website' },
    // Twitter
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: computed(() => settingsStore.settings?.seo_title || 'Il Colle Tinto') },
    { name: 'twitter:description', content: computed(() => settingsStore.settings?.seo_description || 'Vini d\'eccellenza dal Molise.') },
    { name: 'twitter:image', content: computed(() => settingsStore.settings?.seo_image_url || '') },
  ],
  link: [
     { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
});
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
