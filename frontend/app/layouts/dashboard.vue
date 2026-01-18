<script setup>
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
const isSidebarOpen = ref(false);
</script>

<template>
  <div class="flex h-screen bg-stone-50">
    <!-- Desktop Sidebar -->
    <div class="hidden md:block w-64 flex-shrink-0">
        <DashboardSidebar />
    </div>

    <!-- Mobile Sidebar Drawer & Backdrop -->
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
            <div v-if="isSidebarOpen" class="fixed inset-0 bg-stone-900/50 backdrop-blur-sm z-[9998]" @click="isSidebarOpen = false"></div>
        </transition>

        <!-- Sidebar Panel -->
        <transition
            enter-active-class="transition-transform duration-300 ease-in-out"
            enter-from-class="-translate-x-full"
            enter-to-class="translate-x-0"
            leave-active-class="transition-transform duration-300 ease-in-out"
            leave-from-class="translate-x-0"
            leave-to-class="-translate-x-full"
        >
            <div v-if="isSidebarOpen" class="fixed top-0 left-0 bottom-0 w-64 bg-stone-900 z-[9999] md:hidden">
                 <DashboardSidebar @click="isSidebarOpen = false" />
            </div>
        </transition>
    </Teleport>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top Bar (Mobile Toggle + User Info) -->
        <header class="bg-white shadow-sm h-16 flex items-center justify-between px-6 z-10">
            <button @click="isSidebarOpen = true" class="md:hidden text-stone-500 hover:text-stone-800 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
            </button>
            <div class="ml-auto flex items-center gap-4">
                <span class="text-stone-600 text-sm font-medium">{{ user?.full_name || 'Utente' }}</span>
                <div class="h-8 w-8 bg-wine-100 rounded-full flex items-center justify-center text-wine-900 font-bold text-xs ring-2 ring-white shadow-sm">
                    {{ user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U' }}
                </div>
            </div>
        </header>

        <!-- Page Content -->
        <main class="flex-1 overflow-auto p-6 md:p-10">
            <div class="max-w-7xl mx-auto">
                <slot />
            </div>
        </main>
    </div>
  </div>
</template>
