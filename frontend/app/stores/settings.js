
import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
    state: () => ({
        settings: null,
    }),
    actions: {
        async fetchSettings() {
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/settings/`);
                if (!response.ok) throw new Error('Failed to fetch settings');
                this.settings = await response.json();
            } catch (error) {
                console.error('Error fetching settings:', error);
            }
        },
        async updateSettings(settingsData, token) {
            try {
                const config = useRuntimeConfig();
                const response = await fetch(`${config.public.apiBase}/settings/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(settingsData)
                });
                if (!response.ok) throw new Error('Failed to update settings');
                this.settings = await response.json();
                return true;
            } catch (error) {
                console.error('Error updating settings:', error);
                return false;
            }
        }
    }
});
