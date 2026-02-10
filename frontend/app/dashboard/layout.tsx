'use client';

import { ThemeProvider } from '@/lib/theme';
import { ToastProvider } from '@/components/ui/Toast';
import ProtectedRoute from '@/components/auth/protected-route';
import { ReactNode } from 'react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ThemeProvider>
      <ToastProvider>
        <ProtectedRoute>
          <div className="min-h-screen bg-background transition-colors duration-500">
            {/* Main content */}
            <main>
              {children}
            </main>
          </div>
        </ProtectedRoute>
      </ToastProvider>
    </ThemeProvider>
  );
}
