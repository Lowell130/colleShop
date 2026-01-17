
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
                const formData = new FormData();
                formData.append('username', email);
                formData.append('password', password);

                // Use runtime config for base URL in production, hardcode for dev rapid fix
                const response = await fetch('http://localhost:8000/auth/login', {
                    method: 'POST',
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
                const response = await fetch('http://localhost:8000/auth/me', {
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
