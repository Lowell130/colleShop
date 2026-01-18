
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: [],
        isCartOpen: false,
        shippingCost: 0,
        freeShippingThreshold: 100,
    }),
    getters: {
        totalItems: (state) => state.items.reduce((total, item) => total + item.quantity, 0),
        itemsSubtotal: (state) => state.items.reduce((total, item) => total + (item.price * item.quantity), 0),
        shipping: (state) => {
            if (state.items.length === 0) return 0;
            const subtotal = state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
            return subtotal >= state.freeShippingThreshold ? 0 : state.shippingCost;
        },
        totalPrice: (state) => {
            const subtotal = state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
            if (state.items.length === 0) return 0;
            const shipping = subtotal >= state.freeShippingThreshold ? 0 : state.shippingCost;
            return subtotal + shipping;
        },
    },
    actions: {
        initializeCart() {
            if (process.client) {
                const storedCart = localStorage.getItem('cart_items');
                if (storedCart) {
                    try {
                        this.items = JSON.parse(storedCart);
                    } catch (e) {
                        console.error('Failed to parse cart from localStorage', e);
                    }
                }

                // Fetch shipping settings
                this.fetchShippingSettings();
            }
        },
        async fetchShippingSettings() {
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/settings/`);
                if (response.ok) {
                    const settings = await response.json();
                    if (settings.shipping_cost !== undefined) this.shippingCost = settings.shipping_cost;
                    if (settings.free_shipping_threshold !== undefined) this.freeShippingThreshold = settings.free_shipping_threshold;
                }
            } catch (e) {
                console.error("Failed to fetch shipping settings", e);
            }
        },
        addToCart(product, quantity = 1) {
            const productId = product._id || product.id;
            const existingItem = this.items.find(item => item.id === productId);

            if (existingItem) {
                existingItem.quantity += quantity;
            } else {
                // Parse price if it's a string like "€25.00"
                let price = product.price;
                if (typeof price === 'string') {
                    price = parseFloat(price.replace('€', ''));
                }

                this.items.push({
                    id: productId,
                    name: product.name,
                    price: price,
                    image: product.image,
                    type: product.type,
                    quantity: quantity
                });
            }
            // Open cart to confirm addition
            this.isCartOpen = true;
            this.saveCart();
        },
        saveCart() {
            if (process.client) {
                localStorage.setItem('cart_items', JSON.stringify(this.items));
            }
        },
        removeFromCart(productId) {
            const index = this.items.findIndex(item => item.id === productId);
            if (index !== -1) {
                this.items.splice(index, 1);
                this.saveCart();
            }
        },
        toggleCart() {
            this.isCartOpen = !this.isCartOpen;
        },
        incrementItem(productId) {
            const item = this.items.find(i => i.id === productId);
            if (item) {
                item.quantity++;
                this.saveCart();
            }
        },
        decrementItem(productId) {
            const item = this.items.find(i => i.id === productId);
            if (item && item.quantity > 1) {
                item.quantity--;
                this.saveCart();
            } else if (item && item.quantity === 1) {
                this.removeFromCart(productId);
            }
        },
        async checkout(addressData) {
            try {
                const { useAuthStore } = await import('~/stores/auth');
                const authStore = useAuthStore();
                const token = authStore.token;

                if (!token) {
                    throw new Error("Devi effettuare il login per completare l'ordine.");
                }

                const orderData = {
                    items: this.items.map(item => ({
                        product_id: item.id,
                        name: item.name,
                        price: item.price,
                        quantity: item.quantity
                    })),
                    total_amount: this.totalPrice,
                    shipping_address: addressData.shipping_address,
                    billing_address: addressData.billing_address,
                    customer_name: addressData.customer_name, // Optional, can let backend handle from user
                    customer_email: addressData.customer_email, // Optional
                    customer_tax_code: addressData.tax_code
                };

                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/orders/checkout`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(orderData)
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Errore durante il checkout');
                }

                // If success, clear cart
                this.items = [];
                this.saveCart();
                return await response.json();

            } catch (err) {
                console.error("Checkout Error:", err);
                throw err;
            }
        }
    }
});
