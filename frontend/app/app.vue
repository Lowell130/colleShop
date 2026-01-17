import { useSettingsStore } from '~/stores/settings';
import { computed, watchEffect } from 'vue';

const authStore = useAuthStore();
const cartStore = useCartStore();
const settingsStore = useSettingsStore();

authStore.initializeAuth();
cartStore.initializeCart();
settingsStore.fetchSettings();

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

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
