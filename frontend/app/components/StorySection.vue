<script setup>
import { ref } from 'vue';

const isModalOpen = ref(false);

const openModal = (e) => {
  e.preventDefault();
  isModalOpen.value = true;
  document.body.style.overflow = 'hidden'; // Prevent background scrolling
};

const closeModal = () => {
  isModalOpen.value = false;
  document.body.style.overflow = '';
};
</script>

<template>
  <section id="cantina" class="py-20 px-8 bg-white overflow-hidden relative">
    <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
      <!-- Text Content -->
      <div class="order-2 md:order-1">
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">La Nostra Passione</span>
        <h2 class="text-4xl md:text-5xl font-serif text-wine-900 mb-6 leading-tight">La Nostra Storia <br> <span class="italic text-stone-400 font-light">nella terra</span></h2>
        <p class="text-stone-600 mb-6 leading-relaxed text-lg font-light">
          Radicati nella terra del Molise, il nostro viaggio è iniziato con una riverenza per i ritmi della natura. Ogni bottiglia racconta la storia del sole, del vento e delle mani che l'hanno creata.
        </p>
        <p class="text-stone-600 mb-8 leading-relaxed font-light">
          Coltiviamo varietà autoctone con metodi antichi, rispettando la biodiversità del nostro vigneto. Il risultato è un vino sincero, che parla direttamente al cuore.
        </p>
        <a href="#" @click="openModal" class="inline-flex items-center text-wine-900 hover:text-gold-600 font-bold uppercase tracking-widest text-sm transition-colors group">
          Leggi tutto
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </a>
      </div>

      <!-- Image Content -->
      <div class="order-1 md:order-2 relative">
        <div class="absolute -inset-4 bg-gold-200/30 rounded-full transform rotate-6 scale-95 z-0 blur-xl"></div>
        <div class="relative z-10 rounded-sm overflow-hidden shadow-2xl border-4 border-white transform hover:scale-[1.02] transition duration-700">
             <img src="/images/mockup_body.png" alt="Mani nella terra" class="w-full h-auto object-cover" />
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div @click="closeModal" class="absolute inset-0 bg-stone-900/80 backdrop-blur-sm transition-opacity"></div>
        
        <!-- Modal Content -->
        <div class="relative bg-white max-w-2xl w-full max-h-[90vh] overflow-y-auto rounded-sm shadow-2xl p-8 md:p-12 animate-fade-in-up">
          <button @click="closeModal" class="absolute top-4 right-4 text-stone-400 hover:text-wine-900 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          
          <h2 class="text-3xl md:text-4xl font-serif text-wine-900 mb-6">La Nostra Storia Completa</h2>
          
          <div class="prose prose-stone text-stone-600 font-light leading-relaxed space-y-4">
            <p>
              Tutto è iniziato tre generazioni fa, sulle colline ondulate del Molise, dove il sole bacia la terra e il vento accarezza le viti. "Il Colle Tinto" non è solo un'azienda vinicola; è custode di una tradizione che risale a quando il vino si faceva con i piedi e si conservava con il cuore.
            </p>
            <p>
              La nostra filosofia è semplice: <strong>rispetto</strong>. Rispetto per la terra, che nutriamo solo con sostanze organiche. Rispetto per la vite, che potiamo a mano seguendo le fasi lunari. E rispetto per il tempo, perché il buon vino non conosce fretta.
            </p>
            <p>
              Coltiviamo Tintilia, Montepulciano e Falanghina, vitigni che in questo terroir trovano la loro massima espressione. Ogni grappolo viene selezionato manualmente durante la vendemmia, un momento di festa che unisce tutta la famiglia e la comunità locale.
            </p>
            <p>
              La nostra cantina, scavata nella pietra calcarea, mantiene una temperatura costante naturale, ideale per l'affinamento. Qui, in botti di rovere francese e anfore di terracotta, i nostri vini riposano fino a raggiungere quella complessità ed eleganza che li contraddistingue.
            </p>
            <p>
              Oggi, uniamo queste antiche conoscenze alle moderne tecniche di vinificazione per garantire un prodotto salubre, autentico e capace di emozionare. Benvenuti nel nostro mondo, benvenuti a Il Colle Tinto.
            </p>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>
