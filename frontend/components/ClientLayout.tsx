'use client';

import { ThemeProvider } from '@/lib/theme';
import { ToastProvider } from '@/components/ui/Toast';
import Header from '@/components/layout/Header';
import { ReactNode } from 'react';

interface ClientLayoutProps {
  children: ReactNode;
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  return (
    <ThemeProvider>
      <ToastProvider>
        <Header />
        {/* Main content */}
        <main>
          {children}
        </main>
      </ToastProvider>
    </ThemeProvider>
  );
}