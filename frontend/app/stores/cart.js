
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: [],
        isCartOpen: false,
    }),
    getters: {
        totalItems: (state) => state.items.reduce((total, item) => total + item.quantity, 0),
        totalPrice: (state) => state.items.reduce((total, item) => total + (item.price * item.quantity), 0),
    },
    actions: {
        addToCart(product, quantity = 1) {
            const existingItem = this.items.find(item => item.id === product.id);

            if (existingItem) {
                existingItem.quantity += quantity;
            } else {
                this.items.push({
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    image: product.image,
                    type: product.type,
                    quantity: quantity
                });
            }
            // Open cart to confirm addition
            this.isCartOpen = true;
        },
        removeFromCart(productId) {
            const index = this.items.findIndex(item => item.id === productId);
            if (index !== -1) {
                this.items.splice(index, 1);
            }
        },
        toggleCart() {
            this.isCartOpen = !this.isCartOpen;
        },
        incrementItem(productId) {
            const item = this.items.find(i => i.id === productId);
            if (item) item.quantity++;
        },
        decrementItem(productId) {
            const item = this.items.find(i => i.id === productId);
            if (item && item.quantity > 1) {
                item.quantity--;
            } else if (item && item.quantity === 1) {
                this.removeFromCart(productId);
            }
        }
    }
});
