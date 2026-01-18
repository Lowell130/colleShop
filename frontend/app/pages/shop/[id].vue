<script setup>
import { useRoute } from 'vue-router';
import { ref, computed, onMounted, watch } from 'vue';
import { useCartStore } from '~/stores/cart';
import { useProductsStore } from '~/stores/products';
import { storeToRefs } from 'pinia';

const cartStore = useCartStore();
const productsStore = useProductsStore();
const { currentProduct: product } = storeToRefs(productsStore);

const route = useRoute();
const productId = route.params.id;

onMounted(() => {
    productsStore.fetchProduct(productId);
});

// Watch for route changes (if user navigates between products)
watch(
  () => route.params.id,
  (newId) => {
    if (newId) productsStore.fetchProduct(newId);
  }
);

const quantity = ref(1);

const increment = () => quantity.value++;
const decrement = () => { if (quantity.value > 1) quantity.value--; };

const formatPrice = (price) => {
    if (!price) return '€0,00';
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div v-if="product" class="pt-32 pb-20 px-8 bg-white min-h-screen">
    <div class="max-w-7xl mx-auto">
      <!-- Back Link -->
      <button @click="$router.back()" class="flex items-center text-stone-500 hover:text-wine-900 transition-colors mb-10 text-sm font-bold uppercase tracking-widest font-sans">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        Torna allo Shop
      </button>

      <div class="grid md:grid-cols-2 gap-16 items-start">
        <!-- Image Section -->
        <div class="bg-stone-50 rounded-sm p-12 flex items-center justify-center relative overflow-hidden h-[600px]">
           <div class="absolute inset-0 opacity-[0.03] pointer-events-none" style="background-image: url('data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'1\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E');"></div>
           <img v-if="product.image" :src="product.image" :alt="product.name" class="h-full object-contain mix-blend-multiply drop-shadow-2xl">
           <div v-else class="text-stone-300 text-xl font-serif italic">Nessuna Immagine Disponibile</div>
        </div>

        <!-- Info Section -->
        <div>
           <div class="flex items-center gap-4 mb-4">
              <span class="bg-wine-100 text-wine-900 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest">{{ product.type }}</span>
              <span class="text-stone-400 text-sm font-medium">{{ product.year }}</span>
           </div>
           
           <h1 class="text-5xl md:text-6xl font-serif text-stone-900 mb-6 leading-tight">{{ product.name }}</h1>
           <p class="text-2xl text-wine-900 font-serif italic mb-8">{{ formatPrice(product.price) }}</p>
           
           <div class="prose prose-stone text-stone-600 font-light text-lg mb-10 leading-relaxed">
              <p>{{ product.description }}</p>
           </div>
           
           <!-- Tech Specs Grid -->
           <div class="grid grid-cols-2 gap-6 mb-10 border-y border-stone-100 py-8">
              <div>
                 <h4 class="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Vitigno</h4>
                 <p class="text-stone-800 font-medium">{{ product.grape }}</p>
              </div>
              <div>
                 <h4 class="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Gradazione</h4>
                 <p class="text-stone-800 font-medium">{{ product.alcohol }}</p>
              </div>
               <div>
                 <h4 class="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Temperatura</h4>
                 <p class="text-stone-800 font-medium">{{ product.temp }}</p>
              </div>
               <div>
                 <h4 class="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Abbinamenti</h4>
                 <p class="text-stone-800 font-medium">{{ product.pairing }}</p>
              </div>
           </div>

           <!-- Add to Cart -->
           <div class="flex flex-col sm:flex-row gap-6">
              <!-- Quantity -->
              <div class="flex items-center border border-stone-300 rounded-sm w-max" :class="{'opacity-50 pointer-events-none': product.stock <= 0}">
                 <button @click="decrement" class="px-4 py-3 text-stone-500 hover:text-stone-900 transition-colors">-</button>
                 <span class="w-12 text-center font-bold text-stone-900">{{ quantity }}</span>
                 <button @click="increment" class="px-4 py-3 text-stone-500 hover:text-stone-900 transition-colors">+</button>
              </div>

              <button 
                @click="cartStore.addToCart(product, quantity)" 
                :disabled="product.stock <= 0"
                class="flex-grow bg-wine-900 text-white px-10 py-4 rounded-sm font-bold uppercase tracking-widest text-sm hover:bg-wine-800 transition-all duration-300 ease-out shadow-xl hover:shadow-wine-900/30 hover:-translate-y-1 relative overflow-hidden group disabled:bg-stone-300 disabled:text-stone-500 disabled:shadow-none disabled:translate-y-0 disabled:cursor-not-allowed"
              >
                <span v-if="product.stock > 0" class="relative z-10 flex items-center justify-center gap-3">
                   Aggiungi al Carrello 
                   <span class="opacity-70 font-normal">| {{ formatPrice(product.price * quantity) }}</span>
                </span>
                <span v-else class="relative z-10 flex items-center justify-center">
                    Esaurito
                </span>
                <div v-if="product.stock > 0" class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
              </button>
           </div>
           
           <!-- Stock Info -->
           <div class="mt-4 text-xs font-bold uppercase tracking-widest text-right">
                <span v-if="product.stock > 0" class="text-green-600">Disponibilità: {{ product.stock }} pezzi</span>
                <span v-else class="text-red-600">Prodotto Esaurito</span>
           </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center">
      <p class="text-xl text-stone-500">Prodotto non trovato.</p>
  </div>
</template>
