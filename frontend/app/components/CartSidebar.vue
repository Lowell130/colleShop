<script setup>
import { useCartStore } from '~/stores/cart';
import { storeToRefs } from 'pinia';

const cartStore = useCartStore();
const { items, isCartOpen, totalPrice } = storeToRefs(cartStore);

const formatPrice = (price) => {
  return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div>
    <!-- Backdrop -->
    <Transition
      enter-active-class="transition-opacity duration-300 ease-linear"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300 ease-linear"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="isCartOpen" 
        class="fixed inset-0 bg-stone-900/50 backdrop-blur-sm z-[9998]" 
        @click="cartStore.toggleCart()"
      ></div>
    </Transition>

    <!-- Sidebar Panel -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-in-out"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform duration-300 ease-in-out"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div 
        v-if="isCartOpen" 
        class="fixed top-0 right-0 bottom-0 w-full sm:w-[400px] bg-white shadow-2xl z-[9999] flex flex-col h-screen"
      >
        <!-- Header -->
        <div class="p-6 border-b border-stone-100 flex justify-between items-center bg-stone-50">
          <h2 class="text-2xl font-serif text-wine-900">Il Tuo Carrello</h2>
          <button @click="cartStore.toggleCart()" class="text-stone-400 hover:text-wine-900 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Cart Items -->
        <div class="flex-grow overflow-y-auto p-6 space-y-6">
          <div v-if="items.length === 0" class="flex flex-col items-center justify-center h-full text-stone-400">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
             </svg>
             <p>Il carrello è vuoto.</p>
             <button @click="cartStore.toggleCart()" class="mt-4 text-wine-900 font-bold hover:underline">Inizia lo shopping</button>
          </div>

          <div 
            v-else 
            v-for="item in items" 
            :key="item.id" 
            class="flex gap-4 items-start animate-fade-in-up"
          >
            <!-- Image -->
            <div class="w-20 h-20 bg-stone-50 rounded-sm flex items-center justify-center flex-shrink-0">
               <img :src="item.image" :alt="item.name" class="h-16 object-contain mix-blend-multiply">
            </div>

            <!-- Details -->
            <div class="flex-grow">
               <div class="flex justify-between items-start mb-1">
                  <h3 class="font-serif text-stone-900 text-lg leading-tight">{{ item.name }}</h3>
                  <button @click="cartStore.removeFromCart(item.id)" class="text-stone-400 hover:text-red-500 transition-colors ml-2">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                     </svg>
                  </button>
               </div>
               <p class="text-xs text-gold-600 font-bold uppercase tracking-widest mb-2">{{ item.type }}</p>
               
               <div class="flex justify-between items-center">
                  <div class="flex items-center border border-stone-200 rounded-sm">
                     <button @click="cartStore.decrementItem(item.id)" class="px-2 py-1 text-stone-500 hover:text-stone-900 hover:bg-stone-100 transition-colors">-</button>
                     <span class="w-8 text-center text-sm font-medium text-stone-900">{{ item.quantity }}</span>
                     <button @click="cartStore.incrementItem(item.id)" class="px-2 py-1 text-stone-500 hover:text-stone-900 hover:bg-stone-100 transition-colors">+</button>
                  </div>
                  <span class="font-serif text-wine-900 font-medium">{{ formatPrice(item.price * item.quantity) }}</span>
               </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div v-if="items.length > 0" class="p-6 border-t border-stone-100 bg-stone-50">
           <div class="flex justify-between items-center mb-6">
              <span class="text-stone-600 font-medium">Totale</span>
              <span class="text-2xl font-serif text-wine-900">{{ formatPrice(totalPrice) }}</span>
           </div>
           
           <button class="w-full bg-wine-900 text-white py-4 rounded-sm font-bold uppercase tracking-widest text-sm hover:bg-wine-800 transition-all duration-300 ease-out shadow-xl hover:shadow-wine-900/40 hover:-translate-y-1 relative overflow-hidden group">
                <span class="relative z-10">Procedi al Checkout</span>
                <div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
           </button>
        </div>
      </div>
    </Transition>
  </div>
</template>
