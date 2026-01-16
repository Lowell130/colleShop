<script setup>
</script>

<template>
  <section id="cantina" class="py-20 px-8 bg-white overflow-hidden">
    <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
      <!-- Text Content -->
      <div class="order-2 md:order-1">
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">La Nostra Passione</span>
        <h2 class="text-4xl md:text-5xl font-serif text-wine-900 mb-6 leading-tight">La Nostra Storia <br> <span class="italic text-stone-400 font-light">nella terra</span></h2>
        <p class="text-stone-600 mb-6 leading-relaxed text-lg font-light">
          Radicati nella terra del Molise, il nostro viaggio è iniziato con una riverenza per i ritmi della natura. Ogni bottiglia racconta la storia del sole, del vento e delle mani che l'hanno creata.
        </p>
        <p class="text-stone-600 mb-8 leading-relaxed font-light">
          Coltiviamo varietà autoctone con metodi antichi, rispettando la biodiversità del nostro vigneto. Il risultato è un vino sincero, che parla direttamente al cuore.
        </p>
        <a href="#" class="inline-flex items-center text-wine-900 hover:text-gold-600 font-bold uppercase tracking-widest text-sm transition-colors group">
          Leggi tutto
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </a>
      </div>

      <!-- Image Content -->
      <div class="order-1 md:order-2 relative">
        <div class="absolute -inset-4 bg-gold-200/30 rounded-full transform rotate-6 scale-95 z-0 blur-xl"></div>
        <div class="relative z-10 rounded-sm overflow-hidden shadow-2xl border-4 border-white transform hover:scale-[1.02] transition duration-700">
             <img src="/images/mockup_body.png" alt="Mani nella terra" class="w-full h-auto object-cover" />
        </div>
      </div>
    </div>
  </section>
</template>
