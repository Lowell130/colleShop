
import { defineStore } from 'pinia';

export const useProductsStore = defineStore('products', {
    state: () => ({
        products: [],
        currentProduct: null,
        loading: false,
        error: null,
    }),
    getters: {
        getProductById: (state) => (id) => state.products.find(p => p._id === id),
    },
    actions: {
        async fetchProducts() {
            this.loading = true;
            this.error = null;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/products/`);
                if (!response.ok) throw new Error('Failed to fetch products');
                this.products = await response.json();
            } catch (err) {
                this.error = err.message;
                console.error("Error fetching products:", err);
            } finally {
                this.loading = false;
            }
        },

        async fetchProduct(id) {
            this.loading = true;
            this.error = null;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/products/${id}`);
                if (!response.ok) throw new Error('Failed to fetch product');
                this.currentProduct = await response.json();
                return this.currentProduct;
            } catch (err) {
                this.error = err.message;
                console.error("Error fetching product:", err);
                return null; // Return null on error
            } finally {
                this.loading = false;
            }
        },

        async createProduct(productData) {
            this.loading = true;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/products/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(productData)
                });
                if (!response.ok) throw new Error('Failed to create product');
                const newProduct = await response.json();
                this.products.push(newProduct);
                return newProduct;
            } catch (err) {
                this.error = err.message;
                console.error("Error creating product:", err);
                return null;
            } finally {
                this.loading = false;
            }
        },

        async updateProduct(id, productData) {
            this.loading = true;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/products/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(productData)
                });
                if (!response.ok) throw new Error('Failed to update product');
                const updatedProduct = await response.json();
                const index = this.products.findIndex(p => p._id === id);
                if (index !== -1) this.products[index] = updatedProduct;
                this.currentProduct = updatedProduct;
                return updatedProduct;
            } catch (err) {
                this.error = err.message;
                console.error("Error updating product:", err);
                return null;
            } finally {
                this.loading = false;
            }
        },

        async deleteProduct(id) {
            this.loading = true;
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/products/${id}`, {
                    method: 'DELETE'
                });
                if (!response.ok) throw new Error('Failed to delete product');
                this.products = this.products.filter(p => p._id !== id);
                return true;
            } catch (err) {
                this.error = err.message;
                console.error("Error deleting product:", err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        async duplicateProduct(product) {
            const newProductData = { ...product };
            delete newProductData._id; // Remove ID to create new
            newProductData.name = `${newProductData.name} (Copia)`;

            return await this.createProduct(newProductData);
        }
    }
});
