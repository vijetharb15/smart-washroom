import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',  // Add this line to ensure correct path resolution
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  }
  
});
