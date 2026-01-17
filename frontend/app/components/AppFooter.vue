<script setup>
import { useSettingsStore } from '~/stores/settings';
import { onMounted, computed } from 'vue';

const settingsStore = useSettingsStore();

onMounted(() => {
    // Lazy load if not present
    if (!settingsStore.settings) {
        settingsStore.fetchSettings();
    }
});

const s = computed(() => settingsStore.settings || {});
</script>

<template>
  <footer class="bg-[#1c1917] text-stone-300 py-20 px-8 mt-[-20px] relative z-20 overflow-hidden">
    <!-- Decorative Circle -->
    <div class="absolute -top-24 -right-24 w-96 h-96 bg-stone-800 rounded-full blur-3xl opacity-50 pointer-events-none"></div>

    <div class="max-w-6xl mx-auto grid md:grid-cols-4 gap-12 relative z-10">
      <!-- Newsletter -->
      <div class="col-span-1 md:col-span-1">
        <h3 class="font-serif text-2xl text-white mb-6">Resta Aggiornato</h3>
        <p class="text-stone-400 text-sm mb-4 leading-relaxed">
          Iscriviti per ricevere aggiornamenti sulle nostre annate e inviti esclusivi.
        </p>
        <form class="flex flex-col gap-3">
          <input type="email" placeholder="La tua email" class="bg-stone-800/50 border border-stone-700 text-white px-4 py-3 rounded-sm focus:outline-none focus:border-gold-500 transition-colors placeholder-stone-500 text-sm">
          <button class="bg-gold-500 text-stone-900 font-bold uppercase tracking-widest text-xs py-3 rounded-sm hover:bg-gold-400 transition-colors">
            Iscriviti
          </button>
        </form>
      </div>

      <!-- Links 1 -->
      <div>
        <h4 class="font-bold uppercase tracking-widest text-xs text-gold-600 mb-6">Shop</h4>
        <ul class="space-y-3 text-sm">
          <li><a href="#" class="hover:text-white transition-colors">Tutti i Vini</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Rossi</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Bianchi</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Rosati</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Casse Miste</a></li>
        </ul>
      </div>

      <!-- Links 2 -->
      <div>
        <h4 class="font-bold uppercase tracking-widest text-xs text-gold-600 mb-6">L'Azienda</h4>
        <ul class="space-y-3 text-sm">
          <li><a href="#" class="hover:text-white transition-colors">La Nostra Storia</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Il Territorio</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Sostenibilità</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Visite & Degustazioni</a></li>
          <li><a href="/#contatti" class="hover:text-white transition-colors">Contatti</a></li>
          <li class="pt-4 border-t border-stone-800"><NuxtLink to="/login" class="hover:text-white transition-colors text-stone-500">Accesso Area Riservata</NuxtLink></li>
          <li><NuxtLink to="/dashboard" class="hover:text-white transition-colors text-stone-500">Dashboard</NuxtLink></li>
        </ul>
      </div>

      <!-- Contact/Social -->
      <div>
        <h4 class="font-bold uppercase tracking-widest text-xs text-gold-600 mb-6">Il Colle Tinto</h4>
        <p class="text-sm mb-6 leading-relaxed">
          {{ s.address || 'Contrada Colle Tinto, 12, 86010 Castropignano (CB)' }}<br>
          Molise, Italia
        </p>
        <div class="flex gap-4">
           <!-- Social Icons -->
           <a v-if="s.instagram_url" :href="s.instagram_url" target="_blank" class="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center hover:bg-gold-500 hover:text-stone-900 transition-colors cursor-pointer text-xs font-bold text-stone-500">IG</a>
           <a v-if="s.facebook_url" :href="s.facebook_url" target="_blank" class="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center hover:bg-gold-500 hover:text-stone-900 transition-colors cursor-pointer text-xs font-bold text-stone-500">FB</a>
        </div>
      </div>
    </div>

    <div class="border-t border-stone-800 mt-16 pt-8 text-center text-xs text-stone-500 flex flex-col md:flex-row justify-between items-center max-w-6xl mx-auto relative">
      <p>&copy; 2024 Il Colle Tinto. Tutti i diritti riservati.</p>
      
      <div class="flex gap-6 mt-4 md:mt-0">
        <NuxtLink to="/privacy" class="hover:text-stone-300">Privacy Policy</NuxtLink>
        <NuxtLink to="/terms" class="hover:text-stone-300">Termini & Condizioni</NuxtLink>
      </div>
    </div>
  </footer>
</template>
