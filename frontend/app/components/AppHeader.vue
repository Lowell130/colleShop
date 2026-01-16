<script setup>
import { ref } from 'vue';

const links = [
  { name: 'I Nostri Vini', href: '#vini' },
  { name: 'La Cantina', href: '#cantina' },
  { name: 'Sostenibilità', href: '#sostenibilita' },
  { name: 'Contatti', href: '#contatti' },
];

const isMenuOpen = ref(false);
</script>

<template>
  <header class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-8 py-4 text-stone-800 transition-all duration-300 backdrop-blur-sm bg-white/60 border-b border-stone-100/50">
    <!-- Links Left -->
    <nav class="hidden md:flex space-x-8 text-sm uppercase tracking-widest">
      <a v-for="link in links.slice(0, 2)" :key="link.name" :href="link.href" class="font-medium hover:text-gold-600 transition-colors duration-300">
        {{ link.name }}
      </a>
    </nav>

    <!-- Logo Center -->
    <div class="flex flex-col items-center relative z-50">
      <img src="/images/logo.png" alt="Il Colle Tinto" class="h-16 w-auto object-contain drop-shadow-sm transition-transform hover:scale-105 duration-500" />
    </div>

    <!-- Links Right -->
    <nav class="hidden md:flex space-x-8 text-sm uppercase tracking-widest">
      <a v-for="link in links.slice(2)" :key="link.name" :href="link.href" class="font-medium hover:text-gold-600 transition-colors duration-300">
        {{ link.name }}
      </a>
    </nav>

    <!-- Mobile Menu Button -->
    <button @click="isMenuOpen = true" class="md:hidden text-stone-900 focus:outline-none relative z-50">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
      </svg>
    </button>

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
