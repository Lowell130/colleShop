<script setup>
import { ref } from 'vue';

definePageMeta({
    layout: 'default'
});

const email = ref('');
const loading = ref(false);
const message = ref('');
const error = ref('');

const handleSubmit = async () => {
    loading.value = true;
    message.value = '';
    error.value = '';

    try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/auth/forgot-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value })
        });
        
        // Always show success to avoid user enumeration? 
        // Or show generic. Backend returns generic.
        message.value = "Se l'indirizzo email è registrato, riceverai un link per reimpostare la password.";
        email.value = '';
    } catch (e) {
        error.value = "Si è verificato un errore. Riprova più tardi.";
    } finally {
        loading.value = false;
    }
};
</script>

<template>
  <div class="min-h-[70vh] flex flex-col justify-center py-12 px-6 lg:px-8 bg-stone-50">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="text-center text-3xl font-serif text-stone-900 mb-2">Recupero Password</h2>
      <p class="text-center text-stone-600 text-sm">Inserisci la tua email per ricevere le istruzioni.</p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-10 px-10 shadow-sm border border-stone-100 sm:rounded-sm">
        <form v-if="!message" @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="email" class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-1">Email</label>
            <input id="email" v-model="email" type="email" required class="appearance-none block w-full px-3 py-3 border border-stone-300 rounded-sm shadow-sm placeholder-stone-400 focus:outline-none focus:border-wine-900 sm:text-sm transition-colors" placeholder="latua@email.it">
          </div>

          <div>
             <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-sm shadow-sm text-sm font-bold uppercase tracking-widest text-white bg-wine-900 hover:bg-wine-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-wine-900 transition-colors disabled:opacity-50">
                <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></span>
                {{ loading ? 'Invio in corso...' : 'Invia Istruzioni' }}
             </button>
          </div>
          
          <div v-if="error" class="text-red-600 text-sm text-center">
              {{ error }}
          </div>
        </form>

        <div v-else class="text-center animate-fade-in-up">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-800">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
            </div>
            <p class="text-stone-900 font-medium mb-4">{{ message }}</p>
            <NuxtLink to="/login" class="text-wine-900 font-bold hover:underline text-sm uppercase tracking-widest">Torna al Login</NuxtLink>
        </div>

        <div v-if="!message" class="mt-6 text-center">
            <NuxtLink to="/login" class="text-stone-500 hover:text-wine-900 text-xs font-bold uppercase tracking-widest transition-colors">
                Annulla e torna al login
            </NuxtLink>
        </div>

      </div>
    </div>
  </div>
</template>
