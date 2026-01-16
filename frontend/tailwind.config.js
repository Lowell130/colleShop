/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./plugins/**/*.{js,ts}",
        "./app.vue",
        "./error.vue",
    ],
    theme: {
        extend: {
            colors: {
                gold: {
                    50: '#FBF7F1',
                    100: '#F5EEDF',
                    200: '#EBDBBC',
                    300: '#E0C797',
                    400: '#D6B477',
                    500: '#C5A065', // Primary Gold
                    600: '#9E8051',
                    700: '#77603D',
                    800: '#4F4029',
                    900: '#282014',
                },
                wine: {
                    50: '#FDF2F2',
                    100: '#FBE6E6',
                    200: '#F5BFBF',
                    300: '#EF9999',
                    400: '#EA7272',
                    500: '#E44C4C',
                    600: '#B63D3D',
                    700: '#892D2D',
                    800: '#5B1E1E',
                    900: '#4A0404', // Deep Wine
                    950: '#2D0202',
                },
                stone: {
                    50: '#FAFAF9',
                    100: '#F5F5F4',
                    200: '#E7E5E4',
                    300: '#D6D3D1',
                    400: '#A8A29E',
                    500: '#78716C',
                    600: '#57534E',
                    700: '#44403C',
                    800: '#292524',
                    900: '#1C1917',
                    950: '#0C0A09',
                }
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Inter"', 'sans-serif'],
            },
            keyframes: {
                shimmer: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' },
                },
                'fade-in-up': {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            },
            animation: {
                shimmer: 'shimmer 1.5s infinite',
                'fade-in-up': 'fade-in-up 0.8s ease-out forwards',
            }
        },
    },
    plugins: [],
}
