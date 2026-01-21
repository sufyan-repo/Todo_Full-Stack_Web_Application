import { cn } from '@/lib/utils';
import { Inter } from 'next/font/google';
import './globals.css';
import { Suspense } from 'react';
import React from 'react';

const inter = Inter({ subsets: ['latin'] });

// Dynamically import client components to avoid SSR issues
const ClientLayout = React.lazy(() => import('@/components/ClientLayout'));

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-background transition-colors duration-500`}>
        <Suspense fallback={<div className="min-h-screen bg-background" />}>
          <ClientLayout>{children}</ClientLayout>
        </Suspense>
      </body>
    </html>
  );
}