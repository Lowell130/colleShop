
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isAdmin: (state) => state.user?.role === 'admin',
    },
    actions: {
        async initializeAuth() {
            const tokenCookie = useCookie('auth_token');
            const userCookie = useCookie('auth_user');

            if (tokenCookie.value) {
                this.token = tokenCookie.value;
            }
            if (userCookie.value) {
                this.user = userCookie.value;
            }
        },
        setToken(token) {
            this.token = token;
            const cookie = useCookie('auth_token', { maxAge: 60 * 60 * 24 * 7 }); // 7 days
            cookie.value = token;
        },
        setUser(user) {
            this.user = user;
            const cookie = useCookie('auth_user', { maxAge: 60 * 60 * 24 * 7 });
            cookie.value = user;
        },
        async login(email, password) {
            try {
                // Use URLSearchParams for application/x-www-form-urlencoded
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', password);

                const config = useRuntimeConfig();
                // Use runtime config for base URL
                const response = await fetch(`${config.public.apiBase}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formData
                });

                if (!response.ok) {
                    console.error("Login failed");
                    return false;
                }

                const data = await response.json();
                this.setToken(data.access_token);
                this.setUser(data.user);

                return true;
            } catch (e) {
                console.error("Login error", e);
                return false;
            }
        },
        async register(userData) {
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: userData.email,
                        password: userData.password,
                        full_name: userData.fullName // backend expects snake_case
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Registration failed');
                }

                return true;
            } catch (e) {
                console.error("Registration error", e);
                throw e; // Let component handle error message
            }
        },
        logout() {
            this.token = null;
            this.user = null;

            const tokenCookie = useCookie('auth_token');
            const userCookie = useCookie('auth_user');
            tokenCookie.value = null;
            userCookie.value = null;

            const router = useRouter();
            router.push('/login');
        },
        async updateProfile(profileData) {
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/auth/me`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`
                    },
                    body: JSON.stringify(profileData)
                });

                if (!response.ok) throw new Error('Failed to update profile');

                const updatedUser = await response.json();
                this.setUser(updatedUser);
                return true;
            } catch (e) {
                console.error("Profile update error", e);
                throw e;
            }
        }
    }
});
