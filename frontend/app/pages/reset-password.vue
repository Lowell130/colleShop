<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

definePageMeta({
    layout: 'default'
});

const route = useRoute();
const router = useRouter();

const token = route.query.token;
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref('');
const showSuccess = ref(false);

const handleSubmit = async () => {
    error.value = '';
    
    if (password.value !== confirmPassword.value) {
        error.value = "Le password non coincidono.";
        return;
    }
    
    if (password.value.length < 6) {
        error.value = "La password deve essere di almeno 6 caratteri.";
        return;
    }

    loading.value = true;
    try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/auth/reset-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, new_password: password.value })
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Link scaduto o non valido.");
        }

        showSuccess.value = true;
        setTimeout(() => {
            router.push('/login');
        }, 3000);

    } catch (e) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
};
</script>

<template>
  <div class="min-h-[70vh] flex flex-col justify-center py-12 px-6 lg:px-8 bg-stone-50">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="text-center text-3xl font-serif text-stone-900 mb-2">Reimposta Password</h2>
      <p class="text-center text-stone-600 text-sm">Inserisci la tua nuova password.</p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div v-if="!token" class="bg-red-50 p-4 rounded-sm border border-red-200 text-center text-red-800">
          Token mancante. Assicurati di aver cliccato il link dalla mail.
      </div>

      <div v-else class="bg-white py-10 px-10 shadow-sm border border-stone-100 sm:rounded-sm">
        <form v-if="!showSuccess" @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="password" class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-1">Nuova Password</label>
            <input id="password" v-model="password" type="password" required class="appearance-none block w-full px-3 py-3 border border-stone-300 rounded-sm shadow-sm placeholder-stone-400 focus:outline-none focus:border-wine-900 sm:text-sm transition-colors">
          </div>

          <div>
            <label for="confirm" class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-1">Conferma Password</label>
            <input id="confirm" v-model="confirmPassword" type="password" required class="appearance-none block w-full px-3 py-3 border border-stone-300 rounded-sm shadow-sm placeholder-stone-400 focus:outline-none focus:border-wine-900 sm:text-sm transition-colors">
          </div>

          <div>
             <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-sm shadow-sm text-sm font-bold uppercase tracking-widest text-white bg-wine-900 hover:bg-wine-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-wine-900 transition-colors disabled:opacity-50">
                <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></span>
                {{ loading ? 'Updating...' : 'Salva Password' }}
             </button>
          </div>
          
          <div v-if="error" class="text-red-600 text-sm text-center">
              {{ error }}
          </div>
        </form>

        <div v-else class="text-center animate-fade-in-up">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-800">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            </div>
            <p class="text-stone-900 font-bold mb-2">Password Aggiornata!</p>
            <p class="text-stone-600 text-sm mb-4">Verrai reindirizzato al login tra pochi secondi...</p>
        </div>

      </div>
    </div>
  </div>
</template>
