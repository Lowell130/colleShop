<script setup>
import { useCartStore } from '~/stores/cart';
const cartStore = useCartStore();

const wines = [
  {
    id: 1,
    name: 'Verdant Reserve',
    type: 'Bianco',
    price: '€25.00',
    image: '/images/product_placeholder.png' // Clean placeholder
  },
  {
    id: 2,
    name: 'Sun-Drenched Rosé',
    type: 'Rosato',
    price: '€22.00',
    image: '/images/product_placeholder.png'
  },
  {
    id: 3,
    name: 'Earth & Vine',
    type: 'Rosso',
    price: '€28.00',
    image: '/images/product_placeholder.png'
  }
];
</script>

<template>
  <section id="vini" class="py-20 bg-slate-50 relative">
    <!-- Leaves Background Pattern (CSS or SVG) -->
    <div class="absolute inset-0 opacity-5 pointer-events-none overflow-hidden">
        <svg class="absolute top-10 left-0 w-64 h-64 text-gold-500" fill="currentColor" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" /></svg>
        <svg class="absolute bottom-10 right-0 w-96 h-96 text-wine-900" fill="currentColor" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" /></svg>
    </div>

    <div class="max-w-6xl mx-auto px-8 relative z-10">
      <div class="text-center mb-16">
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">La Selezione</span>
        <h2 class="text-4xl md:text-5xl font-serif text-wine-900 mb-4">I Nostri Vini</h2>
        <div class="w-24 h-1 bg-gold-400 mx-auto my-6"></div>
        <p class="text-stone-500 font-light max-w-lg mx-auto">Bottiglie uniche, prodotte in edizione limitata per garantire l'eccellenza in ogni sorso.</p>
      </div>

      <div class="grid md:grid-cols-3 gap-10">
        <div v-for="wine in wines" :key="wine.id" class="bg-white rounded-sm p-8 shadow-sm hover:shadow-2xl hover:shadow-gold-200/50 transition duration-500 group text-center border border-stone-100 relative">
          <div class="h-64 flex items-center justify-center mb-8 relative overflow-hidden rounded-sm bg-stone-50 group-hover:bg-white transition-colors duration-500">
            <!-- Simulated Bottle Image -->
            <img :src="wine.image" class="h-full object-contain mix-blend-multiply group-hover:scale-110 transition duration-700 ease-in-out" :alt="wine.name">
          </div>
          
          <h3 class="text-2xl font-serif text-stone-900 mb-1 group-hover:text-wine-900 transition-colors">{{ wine.name }}</h3>
          <p class="text-xs text-gold-600 font-bold uppercase tracking-widest mb-4">{{ wine.type }}</p>
          <div class="text-xl font-serif text-stone-500 mb-8 italic">{{ wine.price }}</div>
          
          <button @click="cartStore.addToCart(wine)" class="w-full bg-stone-900 text-white py-4 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-900 transition-all duration-300 ease-out flex items-center justify-center gap-2 shadow-md hover:shadow-xl hover:shadow-wine-900/20 hover:-translate-y-1 group">
            <span>Aggiungi al Carrello</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
