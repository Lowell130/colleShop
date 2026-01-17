<script setup>
import { ref } from 'vue';

const links = [
  { name: 'Shop', href: '/shop' },
  { name: 'I Nostri Vini', href: '/#vini' },
  { name: 'La Cantina', href: '/#cantina' },
  { name: 'Sostenibilità', href: '/#sostenibilita' },
  { name: 'Contatti', href: '/#contatti' },
];

import { useAuthStore } from '~/stores/auth';
import { useCartStore } from '~/stores/cart';
import { storeToRefs } from 'pinia';

const cartStore = useCartStore();
const authStore = useAuthStore();
const { totalItems } = storeToRefs(cartStore);

const isMenuOpen = ref(false);
</script>

<template>
  <header class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-8 py-4 text-stone-800 transition-all duration-300 backdrop-blur-sm bg-white/60 border-b border-stone-100/50">
    <!-- Logo Left -->
    <div class="flex flex-col items-center relative z-50 mr-auto">
     <a href="/"> <img src="/images/logo.png" alt="Il Colle Tinto" class="h-16 w-auto object-contain drop-shadow-sm transition-transform hover:scale-105 duration-500" /></a>
    </div>

    <!-- Navigation Right -->
    <nav class="hidden md:flex items-center gap-8 ml-auto">
      <div class="flex space-x-8 text-sm uppercase tracking-widest">
        <a v-for="link in links" :key="link.name" :href="link.href" class="font-medium hover:text-gold-600 transition-colors duration-300">
          {{ link.name }}
        </a>
      </div>
      
      <div class="flex items-center gap-6 pl-8 border-l border-stone-200">
        <!-- User Account -->
        <NuxtLink :to="authStore.token ? '/dashboard' : '/login'" class="text-stone-800 hover:text-wine-900 transition-colors" title="Area Utente">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </NuxtLink>

        <!-- Cart Trigger Desktop -->
        <button @click="cartStore.toggleCart()" class="relative group text-stone-800 hover:text-wine-900 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <span v-if="totalItems > 0" class="absolute -top-2 -right-2 bg-wine-900 text-white text-[10px] font-bold h-5 w-5 rounded-full flex items-center justify-center border-2 border-white transform group-hover:scale-110 transition-transform">
             {{ totalItems }}
          </span>
        </button>
      </div>
    </nav>

    <!-- Mobile Actions (Cart + Menu) -->
    <div class="flex items-center gap-4 md:hidden relative z-50">
        <!-- User Account Mobile -->
        <NuxtLink :to="authStore.token ? '/dashboard' : '/login'" class="text-stone-900 hover:text-wine-900 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </NuxtLink>

        <button @click="cartStore.toggleCart()" class="relative text-stone-900">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span v-if="totalItems > 0" class="absolute -top-1 -right-1 bg-wine-900 text-white text-[9px] font-bold h-4 w-4 rounded-full flex items-center justify-center border border-white">
               {{ totalItems }}
            </span>
        </button>

        <!-- Mobile Menu Button -->
        <button @click="isMenuOpen = true" class="text-stone-900 focus:outline-none">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
    </div>

    <!-- Mobile Menu Drawer & Backdrop -->
    <Teleport to="body">
        <!-- Backdrop -->
        <transition
            enter-active-class="transition-opacity duration-300 ease-linear"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-300 ease-linear"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div v-if="isMenuOpen" class="fixed inset-0 bg-stone-900/50 backdrop-blur-sm z-[9998]" @click="isMenuOpen = false"></div>
        </transition>

        <!-- Drawer Panel -->
        <transition
            enter-active-class="transition-transform duration-300 ease-in-out"
            enter-from-class="-translate-x-full"
            enter-to-class="translate-x-0"
            leave-active-class="transition-transform duration-300 ease-in-out"
            leave-from-class="translate-x-0"
            leave-to-class="-translate-x-full"
        >
            <div v-if="isMenuOpen" class="fixed top-0 left-0 bottom-0 w-4/5 max-w-xs bg-white shadow-2xl z-[9999] p-6 flex flex-col md:hidden h-screen overflow-y-auto">
                <!-- Header of Drawer -->
                <div class="flex justify-between items-center mb-10">
                    <img src="/images/logo.png" alt="Il Colle Tinto" class="h-12 w-auto object-contain" />
                    <button @click="isMenuOpen = false" class="text-stone-500 hover:text-wine-900 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <!-- Links -->
                <nav class="flex flex-col space-y-6">
                    <a 
                      v-for="link in links" 
                      :key="link.name" 
                      :href="link.href" 
                      @click="isMenuOpen = false"
                      class="text-xl font-serif text-stone-800 hover:text-gold-600 transition-colors border-b border-stone-200 pb-2"
                    >
                      {{ link.name }}
                    </a>
                </nav>
                
                <div class="mt-auto text-xs text-stone-400 pt-8">
                    &copy; 2024 Il Colle Tinto
                </div>
            </div>
        </transition>
    </Teleport>
  </header>
</template>
