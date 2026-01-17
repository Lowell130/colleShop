<script setup>
import { useAuthStore } from '../stores/auth';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

definePageMeta({
  layout: false
});

const isLogin = ref(true);
const toggleMode = () => isLogin.value = !isLogin.value;

const form = ref({
    email: '',
    password: '',
    fullName: ''
});

const errorMsg = ref('');

const submit = async () => {
    console.log("Submit clicked! Login mode:", isLogin.value);
    errorMsg.value = '';
    if (isLogin.value) {
        const success = await authStore.login(form.value.email, form.value.password);
        if (success) {
            const redirectParams = route.query.redirect;
            router.push(redirectParams ? decodeURIComponent(redirectParams) : '/dashboard');
        } else {
            errorMsg.value = 'Login fallito. Controlla le credenziali.';
        }
    } else {
        // TODO: Register logic is not yet implemented in store
        alert("La registrazione non è ancora connessa alle API nel frontend, ma le API esistono.");
        console.log("Registering...", form.value);
    }
};
</script>

<template>
  <div class="min-h-screen flex text-stone-800">
    <!-- Left Side: Image -->
    <div class="hidden lg:flex w-1/2 relative overflow-hidden bg-stone-900">
        <img src="/images/story_bg.png" class="absolute inset-0 w-full h-full object-cover opacity-60" />
        <div class="absolute inset-0 bg-gradient-to-r from-stone-900/40 to-black/20"></div>
        <div class="relative z-10 p-20 flex flex-col justify-between h-full text-white">
            <img src="/images/logo.png" class="w-32 brightness-0 invert opacity-90" />
            <div>
                <h1 class="text-5xl font-serif mb-6 leading-tight">Benvenuto a<br/>Il Colle Tinto</h1>
                <p class="text-xl text-stone-300 font-light max-w-md">Scopri l'eccellenza dei nostri vini molisani e gestisci i tuoi ordini con facilità.</p>
            </div>
            <div class="text-stone-500 text-xs">© 2024 Il Colle Tinto. All rights reserved.</div>
        </div>
    </div>

    <!-- Right Side: Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center bg-white p-8 relative">
        <!-- Back to Home Link -->
        <NuxtLink to="/" class="absolute top-8 left-8 text-stone-400 hover:text-wine-900 flex items-center gap-2 transition-colors text-xs font-bold uppercase tracking-widest">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Torna alla Home
        </NuxtLink>

        <div class="max-w-md w-full">
            <div class="mb-12">
                <h2 class="text-3xl font-serif text-stone-900 mb-2">{{ isLogin ? 'Bentornato' : 'Crea Account' }}</h2>
                <p class="text-stone-500 text-sm">
                    {{ isLogin ? 'Inserisci le tue credenziali per accedere.' : 'Registrati per iniziare i tuoi acquisti.' }}
                </p>
                <div v-if="errorMsg" class="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-sm">
                    {{ errorMsg }}
                </div>
            </div>

            <form @submit.prevent="submit" class="space-y-6">
                <div v-if="!isLogin">
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Nome Completo</label>
                    <input v-model="form.fullName" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="Mario Rossi" />
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Email</label>
                    <input v-model="form.email" type="email" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="mario@example.com" />
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Password</label>
                    <input v-model="form.password" type="password" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="••••••••" />
                </div>

                <div v-if="isLogin" class="flex justify-end">
                    <a href="#" class="text-xs text-stone-400 hover:text-wine-900 transition-colors">Password dimenticata?</a>
                </div>

                <button type="submit" class="w-full bg-wine-900 text-white py-4 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all shadow-lg hover:shadow-wine-900/30">
                    {{ isLogin ? 'Accedi' : 'Registrati' }}
                </button>
            </form>

            <div class="mt-8 text-center text-sm text-stone-500">
                {{ isLogin ? 'Non hai un account?' : 'Hai già un account?' }}
                <button @click="toggleMode" class="text-wine-900 font-bold hover:underline ml-1">
                    {{ isLogin ? 'Registrati' : 'Accedi' }}
                </button>
            </div>
        </div>
    </div>
  </div>
</template>
