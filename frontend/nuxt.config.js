export default defineNuxtConfig({
    modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
    devtools: { enabled: true },
    future: {
        compatibilityVersion: 4,
    },
    compatibilityDate: '2024-11-01',
    app: {
        head: {
            link: [
                { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap' }
            ]
        }
    }
});
