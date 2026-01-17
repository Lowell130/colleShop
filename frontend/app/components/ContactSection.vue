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

const bookingLink = computed(() => {
    return s.value.booking_email ? `mailto:${s.value.booking_email}?subject=Prenotazione Degustazione` : '#';
});
</script>

<template>
  <section id="contatti" class="py-24 bg-white relative">
    <div class="max-w-6xl mx-auto px-8">
      <div class="text-center mb-16">
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">Vieni a trovarci</span>
        <h2 class="text-4xl md:text-5xl font-serif text-wine-900 mb-6">Contatti & Visite</h2>
        <p class="text-stone-500 font-light max-w-lg mx-auto">Saremo lieti di accoglierti in cantina per una degustazione o semplicemente per mostrarti le nostre vigne.</p>
      </div>

      <div class="grid md:grid-cols-2 gap-12 bg-stone-50 p-8 md:p-12 rounded-sm shadow-xl border border-stone-100">
        <!-- Contact Info -->
        <div class="space-y-8">
          <div>
            <h3 class="text-2xl font-serif text-stone-800 mb-4">I Nostri Recapiti</h3>
            <p v-if="s.address" class="text-stone-600 mb-2 font-light"><strong class="font-medium text-stone-900">Indirizzo:</strong> {{ s.address }}</p>
            <p v-if="s.email" class="text-stone-600 mb-2 font-light"><strong class="font-medium text-stone-900">Email:</strong> {{ s.email }}</p>
            <p v-if="s.phone" class="text-stone-600 mb-2 font-light"><strong class="font-medium text-stone-900">Telefono:</strong> {{ s.phone }}</p>
          </div>
          
          <div>
            <h3 class="text-2xl font-serif text-stone-800 mb-4">Orari Cantina</h3>
            <ul class="space-y-2 text-stone-600 font-light">
                <li v-if="s.hours_weekdays" class="flex justify-between border-b border-stone-200 pb-2"><span>Lun - Ven</span> <span>{{ s.hours_weekdays }}</span></li>
                <li v-if="s.hours_saturday" class="flex justify-between border-b border-stone-200 pb-2"><span>Sabato</span> <span>{{ s.hours_saturday }}</span></li>
                <li v-if="s.hours_sunday" class="flex justify-between pb-2"><span>Domenica</span> <span>{{ s.hours_sunday }}</span></li>
            </ul>
          </div>
          
          <div class="pt-4">
             <a :href="bookingLink" class="w-full bg-wine-900 text-white py-4 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all duration-300 ease-out shadow-lg hover:shadow-xl hover:shadow-wine-900/30 hover:-translate-y-1 relative overflow-hidden group block text-center">
                <span class="relative z-10">Prenota una Degustazione</span>
                <div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
             </a>
          </div>
        </div>

        <!-- Map Placeholder -->
        <div class="h-96 md:h-auto bg-stone-200 rounded-sm relative overflow-hidden group">
            <template v-if="s.google_maps_url">
                <iframe 
                    :src="s.google_maps_url" 
                    width="100%" 
                    height="100%" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy" 
                    referrerpolicy="no-referrer-when-downgrade"
                    class="absolute inset-0 w-full h-full grayscale opacity-80 hover:grayscale-0 hover:opacity-100 transition-all duration-700">
                </iframe>
            </template>
            <template v-else>
                 <div class="absolute inset-0 flex items-center justify-center text-stone-500 font-serif z-10">Mappa (Google Maps Placeholder)</div>
                 <img src="/images/mockup_hero.png" class="absolute inset-0 w-full h-full object-cover opacity-20 grayscale group-hover:grayscale-0 transition duration-700" />
            </template>
        </div>
      </div>
    </div>
  </section>
</template>
