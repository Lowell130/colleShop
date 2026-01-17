<script setup>
import { useProductsStore } from '~/stores/products';
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const route = useRoute();
const router = useRouter();
const productsStore = useProductsStore();
const { loading } = storeToRefs(productsStore);

const isNew = route.params.id === 'new';

const form = ref({
    name: '',
    type: 'Rosso',
    price: 0,
    description: '',
    grape: '',
    year: new Date().getFullYear().toString(),
    alcohol: '',
    temp: '',
    pairing: '',
    image: '/images/product_placeholder.png' // Default placeholder
});

onMounted(async () => {
    if (!isNew) {
        const product = await productsStore.fetchProduct(route.params.id);
        if (product) {
            form.value = { ...product };
        } else {
            router.push('/dashboard/products'); // Redirect if not found
        }
    }
});

const save = async () => {
    let result;
    if (isNew) {
        result = await productsStore.createProduct(form.value);
    } else {
        result = await productsStore.updateProduct(route.params.id, form.value);
    }

    if (result) {
        router.push('/dashboard/products');
    } else {
        alert("Errore durante il salvataggio.");
    }
};
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-center gap-4 mb-8">
        <NuxtLink to="/dashboard/products" class="text-stone-400 hover:text-stone-900 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
        </NuxtLink>
        <h1 class="text-3xl font-serif text-stone-900">{{ isNew ? 'Nuovo Vino' : 'Modifica Vino' }}</h1>
    </div>

    <div class="bg-white p-8 rounded-sm shadow-sm border border-stone-100 relative">
        <div v-if="loading" class="absolute inset-0 bg-white/80 z-10 flex items-center justify-center">
             <span class="text-wine-900 font-bold animate-pulse">Salvataggio in corso...</span>
        </div>

        <form @submit.prevent="save" class="space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Left Column: Image -->
                <div>
                     <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Immagine (URL)</label>
                     <input v-model="form.image" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors mb-4" placeholder="/images/..." />
                     
                     <div class="bg-stone-50 border border-stone-100 rounded-sm p-4 flex items-center justify-center h-64 sticky top-4">
                         <img :src="form.image" @error="$event.target.src='/images/product_placeholder.png'" class="max-h-full object-contain" />
                     </div>
                </div>

                <!-- Right Column: Details -->
                <div class="space-y-6">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Nome Vino</label>
                        <input v-model="form.name" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" required />
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Tipologia</label>
                            <select v-model="form.type" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors">
                                <option value="Rosso">Rosso</option>
                                <option value="Bianco">Bianco</option>
                                <option value="Rosato">Rosato</option>
                                <option value="Spumante">Spumante</option>
                            </select>
                        </div>
                         <div>
                             <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Prezzo (€)</label>
                             <input v-model="form.price" type="number" step="0.01" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" required />
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                             <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Vitigno</label>
                             <input v-model="form.grape" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" />
                        </div>
                        <div>
                             <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Annata</label>
                             <input v-model="form.year" type="number" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" />
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                         <div>
                             <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Alcol</label>
                             <input v-model="form.alcohol" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="14%" />
                        </div>
                        <div>
                             <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Temperatura</label>
                             <input v-model="form.temp" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="18°C" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Full Width Fields -->
             <div>
                 <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Abbinamenti</label>
                 <input v-model="form.pairing" type="text" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors" placeholder="Carni rosse, formaggi..." />
            </div>

            <div>
                 <label class="block text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Descrizione</label>
                 <textarea v-model="form.description" rows="4" class="w-full px-4 py-3 bg-stone-50 border border-stone-200 rounded-sm focus:outline-none focus:border-wine-900 transition-colors"></textarea>
            </div>
            
            <div class="pt-6 border-t border-stone-100 flex justify-end gap-4">
                <NuxtLink to="/dashboard/products" class="px-6 py-3 text-stone-500 hover:text-stone-900 transition-colors font-medium">Annulla</NuxtLink>
                <button type="submit" class="bg-wine-900 text-white px-8 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all shadow-md hover:shadow-lg">
                    {{ isNew ? 'Crea Vino' : 'Salva Modifiche' }}
                </button>
            </div>
        </form>
    </div>
  </div>
</template>
