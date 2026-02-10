'use client';

import { ReactNode, useState, useEffect } from 'react';
import ClientLayout from '@/components/ClientLayout';

export default function ClientLayoutWrapper({ children }: { children: ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    // Return the same structure as ClientLayout during SSR to prevent hydration mismatch
    return <div className="min-h-screen bg-background">{children}</div>;
  }

  return <ClientLayout>{children}</ClientLayout>;
}