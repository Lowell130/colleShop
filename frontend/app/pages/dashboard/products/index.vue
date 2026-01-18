<script setup>
import { useProductsStore } from '~/stores/products';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
});

const productsStore = useProductsStore();
const { products, loading } = storeToRefs(productsStore);

onMounted(() => {
    productsStore.fetchProducts();
});

const handleDelete = async (id) => {
    if(confirm('Sei sicuro di voler eliminare questo vino?')) {
        await productsStore.deleteProduct(id);
    }
};

const handleDuplicate = async (product) => {
    if(confirm(`Vuoi duplicare ${product.name}?`)) {
        await productsStore.duplicateProduct(product);
    }
};
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-serif text-stone-900">Gestione Prodotti</h1>
        <NuxtLink to="/dashboard/products/new" class="bg-wine-900 text-white px-6 py-3 rounded-sm font-bold uppercase tracking-widest text-xs hover:bg-wine-800 transition-all shadow-md">
            + Nuovo Vino
        </NuxtLink>
    </div>

    <!-- Products Table -->
    <div class="bg-white rounded-sm shadow-sm border border-stone-100 overflow-hidden relative">
        <div v-if="loading" class="absolute inset-0 bg-white/80 z-10 flex items-center justify-center">
            <span class="text-wine-900 font-bold animate-pulse">Caricamento...</span>
        </div>

        <table class="w-full text-left">
            <thead class="bg-stone-50 border-b border-stone-200">
                <tr>
                    <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-stone-500">Nome</th>
                    <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-stone-500">Tipo</th>
                    <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-stone-500">Stock</th>
                    <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-stone-500">Prezzo</th>
                    <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-stone-500 text-right">Azioni</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-stone-100">
                <tr v-if="products.length === 0 && !loading">
                     <td colspan="5" class="px-6 py-8 text-center text-stone-400">Nessun prodotto trovato.</td>
                </tr>

                <tr v-for="product in products" :key="product._id" class="hover:bg-stone-50/50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <img v-if="product.image" :src="product.image" class="h-10 w-10 object-cover rounded-sm bg-stone-100" />
                            <div v-else class="h-10 w-10 bg-stone-100 rounded-sm flex items-center justify-center text-stone-300 text-xs">IMG</div>
                            <span class="font-medium text-stone-800">{{ product.name }}</span>
                        </div>
                    </td>
                    <td class="px-6 py-4 text-stone-600">{{ product.type }}</td>
                    <td class="px-6 py-4">
                        <span :class="{'text-red-600 font-bold': product.stock <= 0, 'text-green-600': product.stock > 0}">
                            {{ product.stock || 0 }}
                        </span>
                    </td>
                    <td class="px-6 py-4 font-serif text-lg text-stone-800">€ {{ product.price.toFixed(2) }}</td>
                    <td class="px-6 py-4 text-right flex justify-end gap-3">
                        <button @click="handleDuplicate(product)" class="text-stone-400 hover:text-gold-600 transition-colors" title="Duplica">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                            </svg>
                        </button>
                        <NuxtLink :to="`/dashboard/products/${product._id}`" class="text-stone-400 hover:text-wine-900 transition-colors" title="Modifica">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                            </svg>
                        </NuxtLink>
                        <button @click="handleDelete(product._id)" class="text-stone-400 hover:text-red-900 transition-colors" title="Elimina">
                             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                            </svg>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>
