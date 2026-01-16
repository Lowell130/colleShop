<script setup>
</script>

<template>
  <div class="font-sans text-slate-900 bg-slate-50 min-h-screen flex flex-col">
    <AppHeader />
    <div class="flex-grow">
      <slot />
    </div>
    <AppFooter />
    <CartSidebar />
  </div>
</template>
