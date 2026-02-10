'use client';

import { ReactNode, useEffect, useState } from 'react';

interface NoSSRWrapperProps {
  children: ReactNode;
}

/**
 * NoSSRWrapper component
 * Ensures children are only rendered on the client side to prevent hydration mismatches
 */
export default function NoSSRWrapper({ children }: NoSSRWrapperProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return isMounted ? <>{children}</> : <div className="min-h-screen bg-background" />;
}