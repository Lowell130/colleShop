<template>
  <section id="sostenibilita" class="py-24 bg-stone-100 relative overflow-hidden">
    <!-- Decorative Pattern -->
    <div class="absolute inset-0 opacity-[0.03] pointer-events-none" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>

    <div class="max-w-6xl mx-auto px-8 grid md:grid-cols-2 gap-16 items-center relative z-10">
      <div class="relative">
        <div class="absolute -inset-4 bg-green-200/30 rounded-full blur-2xl z-0"></div>
        <img src="/images/mockup_body.png" alt="Sostenibilità in Vigna" class="relative z-10 rounded-sm shadow-xl grayscale hover:grayscale-0 transition duration-700 ease-in-out object-cover h-[500px] w-full" />
        <div class="absolute bottom-10 -right-10 bg-white p-6 shadow-lg max-w-xs hidden md:block z-20 border-l-4 border-gold-500">
           <p class="font-serif italic text-wine-900 text-lg">"La terra non ci è stata donata dai nostri padri, ma prestata dai nostri figli."</p>
        </div>
      </div>

      <div>
        <span class="text-gold-600 uppercase tracking-widest text-xs font-bold mb-2 block">Il Nostro Impegno</span>
        <h2 class="text-4xl md:text-5xl font-serif text-wine-900 mb-8 leading-tight">Sostenibilità <br> <span class="italic text-stone-400 font-light">Radicale</span></h2>
        
        <div class="space-y-8">
          <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-green-900/10 rounded-full flex items-center justify-center text-green-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <div>
              <h3 class="text-xl font-serif text-stone-800 mb-2">Biodiversità</h3>
              <p class="text-stone-600 font-light leading-relaxed">Lasciamo che erbe spontanee e fiori crescano tra i filari, creando un ecosistema vivo che protegge le viti naturalmente.</p>
            </div>
          </div>

          <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-green-900/10 rounded-full flex items-center justify-center text-green-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
            </div>
            <div>
              <h3 class="text-xl font-serif text-stone-800 mb-2">Energia Pulita</h3>
              <p class="text-stone-600 font-light leading-relaxed">Tutta la nostra cantina è alimentata da pannelli solari, riducendo al minimo l'impatto carbonico della produzione.</p>
            </div>
          </div>
          
           <div class="flex gap-4">
            <div class="flex-shrink-0 w-12 h-12 bg-green-900/10 rounded-full flex items-center justify-center text-green-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
            </div>
            <div>
              <h3 class="text-xl font-serif text-stone-800 mb-2">Nessuna Chimica</h3>
              <p class="text-stone-600 font-light leading-relaxed">Rifiutiamo diserbanti e pesticidi sistemici. Usiamo solo rame, zolfo e preparati naturali.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
