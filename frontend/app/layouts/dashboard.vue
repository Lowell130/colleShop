<script setup>
import { useAuthStore } from '~/stores/auth';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { isAdmin, user } = storeToRefs(authStore);
const router = useRouter();

const commonLinks = [
  { name: 'Overview', href: '/dashboard', icon: 'M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z' },
  { name: 'Ordini', href: '/dashboard/orders', icon: 'M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z' },
  { name: 'Profilo', href: '/dashboard/profile', icon: 'M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z' },
];

const adminLinks = [
  { name: 'Gestione Prodotti', href: '/dashboard/products', icon: 'M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5' },
  { name: 'Impostazioni', href: '/dashboard/settings', icon: 'M10.34 1.503a.375.375 0 01.61 0l.432.923c.3.643.694 1.243 1.174 1.772l.923-.274a.375.375 0 01.444.156l1.24 2.148a.375.375 0 01-.115.485l-1.01.762a7.513 7.513 0 010 3.056l1.01.762a.375.375 0 01.115.485l-1.24 2.148a.375.375 0 01-.444.156l-.924-.274a7.515 7.515 0 01-1.174 1.773l-.432.922a.375.375 0 01-.61 0l-.432-.922a7.515 7.515 0 01-1.174-1.773l-.923.274a.375.375 0 01-.444-.156l-1.24-2.148a.375.375 0 01.115-.485l1.01-.762a7.513 7.513 0 010-3.056l-1.01-.762a.375.375 0 01-.115-.485l1.24-2.148a.375.375 0 01.444-.156l.923.274c.48-.529.874-1.13 1.174-1.772l.432-.923zM10.5 13.5a3 3 0 100-6 3 3 0 000 6z' },
];

const links = computed(() => {
    return isAdmin.value ? [...commonLinks, ...adminLinks] : commonLinks;
});


</script>

<template>
  <div class="flex h-screen bg-stone-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-stone-900 text-white flex-shrink-0 hidden md:flex flex-col">
      <div class="p-6 border-b border-stone-800 flex justify-center">
         <img src="/images/logo.png" alt="Logo" class="h-12 w-auto brightness-0 invert opacity-80" />
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <NuxtLink v-for="link in links" :key="link.name" :to="link.href" 
           class="flex items-center gap-3 px-4 py-3 rounded-sm transition-colors text-stone-300 hover:bg-stone-800 hover:text-white"
           active-class="bg-wine-900 text-white shadow-lg">
           <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
             <path stroke-linecap="round" stroke-linejoin="round" :d="link.icon" />
           </svg>
           <span class="font-medium tracking-wide text-sm">{{ link.name }}</span>
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-stone-800">
        <button @click="authStore.logout()" class="flex items-center gap-2 text-stone-400 hover:text-white transition-colors w-full px-4 py-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
            </svg>
            <span class="text-sm">Logout</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top Bar (Mobile Toggle + User Info) -->
        <header class="bg-white shadow-sm h-16 flex items-center justify-between px-6 z-10">
            <button class="md:hidden text-stone-500">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
            </button>
            <div class="ml-auto flex items-center gap-4">
                <span class="text-stone-600 text-sm font-medium">{{ user?.fullName || 'Utente' }}</span>
                <div class="h-8 w-8 bg-wine-100 rounded-full flex items-center justify-center text-wine-900 font-bold text-xs ring-2 ring-white shadow-sm">
                    {{ user?.fullName ? user.fullName.charAt(0).toUpperCase() : 'U' }}
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
