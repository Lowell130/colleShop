<script setup>
import { useRoute } from 'vue-router';
import { ref, computed } from 'vue';
import { useCartStore } from '~/stores/cart';

const cartStore = useCartStore();

const route = useRoute();
const productId = computed(() => parseInt(route.params.id));

// Mock Data (Same as index.vue - ideal to unify later)
const products = [
  {
    id: 1,
    name: 'Verdant Reserve',
    type: 'Bianco',
    price: 25.00,
    image: '/images/product_placeholder.png',
    description: 'Un bianco strutturato e complesso, con note di fiori bianchi, pesca gialla e un tocco di mandorla tostata. Perfetto per accompagnare piatti di pesce strutturati o formaggi a media stagionatura.',
    grape: 'Falanghina 100%',
    year: '2022',
    alcohol: '13.5%',
    temp: '10-12°C',
    pairing: 'Pesce al forno, Risotti, Formaggi freschi'
  },
  {
    id: 2,
    name: 'Sun-Drenched Rosé',
    type: 'Rosato',
    price: 22.00,
    image: '/images/product_placeholder.png',
    description: 'Fresco e minerale, questo rosato cattura l\'essenza delle serate estive. Sentori di fragolina di bosco e rosa canina. Ideale come aperitivo.',
    grape: 'Tintilia 100%',
    year: '2023',
    alcohol: '12.5%',
    temp: '8-10°C',
    pairing: 'Aperitivi, Crostacei, Salumi leggeri'
  },
  {
    id: 3,
    name: 'Earth & Vine',
    type: 'Rosso',
    price: 28.00,
    image: '/images/product_placeholder.png',
    description: 'Un rosso intenso che racconta la forza della terra molisana. Note di amarena, cuoio e spezie dolci. Tannino morbido e persistente.',
    grape: 'Montepulciano 100%',
    year: '2020',
    alcohol: '14.5%',
    temp: '16-18°C',
    pairing: 'Carni rosse, Cacciagione, Formaggi stagionati'
  },
   {
    id: 4,
    name: 'Midnight Reserve',
    type: 'Rosso',
    price: 45.00,
    image: '/images/product_placeholder.png',
    description: 'La nostra riserva più prestigiosa, invecchiata 24 mesi in barrique. Un vino da meditazione, profondo ed elegante.',
    grape: 'Tintilia 100%',
    year: '2019',
    alcohol: '15%',
    temp: '18°C',
    pairing: 'Arrosti importanti, Cioccolato fondente'
  },
    {
    id: 5,
    name: 'Golden Breeze',
    type: 'Bianco',
    price: 18.00,
    image: '/images/product_placeholder.png',
    description: 'Leggero e beverino, ideale per piatti di pesce. Sentori di mela verde e fiori di campo.',
    grape: 'Trebbiano 100%',
    year: '2023',
    alcohol: '12%',
    temp: '8-10°C',
    pairing: 'Antipasti di mare, Fritture'
  }
];

const product = computed(() => products.find(p => p.id === productId.value));

const quantity = ref(1);

const increment = () => quantity.value++;
const decrement = () => { if (quantity.value > 1) quantity.value--; };

const formatPrice = (price) => {
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
           <img :src="product.image" :alt="product.name" class="h-full object-contain mix-blend-multiply drop-shadow-2xl">
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
              <div class="flex items-center border border-stone-300 rounded-sm w-max">
                 <button @click="decrement" class="px-4 py-3 text-stone-500 hover:text-stone-900 transition-colors">-</button>
                 <span class="w-12 text-center font-bold text-stone-900">{{ quantity }}</span>
                 <button @click="increment" class="px-4 py-3 text-stone-500 hover:text-stone-900 transition-colors">+</button>
              </div>

              <button @click="cartStore.addToCart(product, quantity)" class="flex-grow bg-wine-900 text-white px-10 py-4 rounded-sm font-bold uppercase tracking-widest text-sm hover:bg-wine-800 transition-all duration-300 ease-out shadow-xl hover:shadow-wine-900/30 hover:-translate-y-1 relative overflow-hidden group">
                <span class="relative z-10 flex items-center justify-center gap-3">
                   Aggiungi al Carrello 
                   <span class="opacity-70 font-normal">| {{ formatPrice(product.price * quantity) }}</span>
                </span>
                <div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
              </button>
           </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center">
      <p class="text-xl text-stone-500">Prodotto non trovato.</p>
  </div>
</template>
