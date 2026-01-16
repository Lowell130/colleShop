<script setup>
import { ref, computed } from 'vue';
import { useCartStore } from '~/stores/cart';

const cartStore = useCartStore();

// Mock Data (Ideally moved to a composable or store later)
const products = [
  {
    id: 1,
    name: 'Verdant Reserve',
    type: 'Bianco',
    price: 25.00,
    image: '/images/product_placeholder.png',
    description: 'Un bianco strutturato e complesso, con note di fiori bianchi e agrumi.',
    grape: 'Falanghina',
    year: '2022'
  },
  {
    id: 2,
    name: 'Sun-Drenched Rosé',
    type: 'Rosato',
    price: 22.00,
    image: '/images/product_placeholder.png',
    description: 'Fresco e minerale, perfetto per aperitivi al tramonto.',
    grape: 'Tintilia',
    year: '2023'
  },
  {
    id: 3,
    name: 'Earth & Vine',
    type: 'Rosso',
    price: 28.00,
    image: '/images/product_placeholder.png',
    description: 'Un rosso intenso che racconta la forza della terra molisana.',
    grape: 'Montepulciano',
    year: '2020'
  },
  {
    id: 4,
    name: 'Midnight Reserve',
    type: 'Rosso',
    price: 45.00,
    image: '/images/product_placeholder.png',
    description: 'La nostra riserva più prestigiosa, invecchiata 24 mesi in barrique.',
    grape: 'Tintilia',
    year: '2019'
  },
    {
    id: 5,
    name: 'Golden Breeze',
    type: 'Bianco',
    price: 18.00,
    image: '/images/product_placeholder.png',
    description: 'Leggero e beverino, ideale per piatti di pesce.',
    grape: 'Trebbiano',
    year: '2023'
  }
];

// Filtering Logic
const activeFilter = ref('Tutti');
const filters = ['Tutti', 'Rosso', 'Bianco', 'Rosato'];

const filteredProducts = computed(() => {
  if (activeFilter.value === 'Tutti') return products;
  return products.filter(p => p.type === activeFilter.value);
});

// Format Price
const formatPrice = (price) => {
  return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div class="pt-32 pb-20 px-8 bg-stone-50 min-h-screen">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-16">
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">La Collezione Completa</span>
        <h1 class="text-5xl md:text-6xl font-serif text-wine-900 mb-6">La Nostra Cantina</h1>
        <p class="text-stone-500 font-light max-w-lg mx-auto text-lg">Esplora la nostra selezione di vini unici, frutto di passione e tradizione.</p>
      </div>

      <!-- Filters -->
      <div class="flex justify-center flex-wrap gap-4 mb-16">
        <button 
          v-for="filter in filters" 
          :key="filter"
          @click="activeFilter = filter"
          :class="[
            'px-8 py-3 rounded-full text-sm font-bold uppercase tracking-widest transition-all duration-300 border',
            activeFilter === filter 
              ? 'bg-wine-900 text-white border-wine-900 shadow-lg' 
              : 'bg-white text-stone-500 border-stone-200 hover:border-wine-900 hover:text-wine-900'
          ]"
        >
          {{ filter }}
        </button>
      </div>

      <!-- Product Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id"
          class="bg-white rounded-sm p-8 shadow-sm hover:shadow-2xl hover:shadow-gold-200/50 transition duration-500 group text-center border border-stone-100 flex flex-col"
        >
          <!-- Image -->
          <div class="h-64 flex items-center justify-center mb-8 relative overflow-hidden rounded-sm bg-stone-50 group-hover:bg-white transition-colors duration-500 cursor-pointer" @click="$router.push(`/shop/${product.id}`)">
             <img :src="product.image" :alt="product.name" class="h-full object-contain mix-blend-multiply group-hover:scale-110 transition duration-700 ease-in-out">
          </div>
          
          <!-- Content -->
          <div class="flex-grow">
            <div class="text-xs text-gold-600 font-bold uppercase tracking-widest mb-1">{{ product.grape }} — {{ product.year }}</div>
            <h3 class="text-2xl font-serif text-stone-900 mb-2 group-hover:text-wine-900 transition-colors cursor-pointer" @click="$router.push(`/shop/${product.id}`)">{{ product.name }}</h3>
            <p class="text-stone-500 font-light text-sm mb-4 line-clamp-2">{{ product.description }}</p>
            <div class="text-xl font-serif text-stone-900 mb-6 font-medium italic">{{ formatPrice(product.price) }}</div>
          </div>

          <!-- Actions -->
          <div class="mt-auto space-y-3">
             <button @click="cartStore.addToCart(product)" class="w-full bg-stone-900 text-white py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-900 transition-all duration-300 ease-out flex items-center justify-center gap-2 shadow-md hover:shadow-xl hover:shadow-wine-900/20 hover:-translate-y-1 group/btn">
                <span>Aggiungi al Carrello</span>
             </button>
             <button @click="$router.push(`/shop/${product.id}`)" class="w-full bg-transparent text-stone-500 py-2 rounded-sm font-bold uppercase tracking-widest text-[10px] hover:text-wine-900 transition-colors">
                Visualizza Dettagli
             </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
