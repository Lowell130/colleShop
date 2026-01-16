<script setup>
</script>

<template>
  <section class="relative h-screen min-h-[700px] flex items-center justify-center overflow-hidden bg-stone-50">
    <!-- Background Image -->
    <div class="absolute inset-0 z-0">
      <img src="/images/mockup_hero.png" alt="Vigneto Molisano" class="w-full h-full object-cover object-top" />
      <!-- Radial Overlay for Light & Readability Center Focus -->
      <div class="absolute inset-0 bg-gradient-to-r from-white/50 via-white/70 to-white/50 backdrop-blur-[2px]"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-white/90 via-transparent to-white/30"></div>
    </div>

    <!-- Content Container -->
    <div class="relative z-10 text-center px-4 pt-24 max-w-5xl mx-auto">
      <span class="block text-gold-700 tracking-[0.3em] uppercase text-sm font-bold mb-4 animate-fade-in-up drop-shadow-sm">Eredità Molisana</span>
      <h1 class="text-6xl md:text-8xl font-serif text-stone-900 mb-6 drop-shadow-sm leading-tight animate-fade-in-up delay-100">
        Vini Naturali <br /> <span class="italic text-wine-900 font-light">di Carattere</span>
      </h1>
      <p class="text-lg md:text-2xl text-stone-800 mb-12 font-medium max-w-2xl mx-auto leading-relaxed animate-fade-in-up delay-200">
        Dalla terra al bicchiere. Un viaggio sensoriale attraverso <br class="hidden md:block"> la tradizione e l'autenticità del Molise.
      </p>
      
      <!-- CTA Buttons -->
      <div class="flex flex-col md:flex-row justify-center gap-6 animate-fade-in-up delay-300">
        <button class="bg-wine-900 text-white px-10 py-4 rounded-sm hover:bg-wine-800 transition-all duration-300 ease-out shadow-xl hover:shadow-wine-900/40 hover:-translate-y-1 uppercase tracking-widest text-sm font-bold relative overflow-hidden group">
          <span class="relative z-10">Scopri i Vini</span>
          <div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
        </button>
        <button class="bg-white/80 backdrop-blur-sm text-stone-900 border border-stone-200 px-10 py-4 rounded-sm hover:bg-stone-900 hover:text-white hover:border-stone-900 transition-all duration-300 ease-out shadow-sm hover:shadow-lg hover:-translate-y-1 uppercase tracking-widest text-sm font-bold">
          La Nostra Storia
        </button>
      </div>
    </div>
  </section>
</template>
