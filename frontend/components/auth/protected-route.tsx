'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';
import { Spinner } from '@/components/ui/spinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode; // Custom fallback component
}

export default function ProtectedRoute({ children, fallback }: ProtectedRouteProps) {
  const [loading, setLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      // Only check authentication once on mount
      const authStatus = isAuthenticated();
      setIsAuth(authStatus);

      if (!authStatus) {
        // Redirect to sign-in if not authenticated
        router.replace('/auth/sign-in'); // Using replace to avoid back button issues
      }

      setLoading(false);
    };

    checkAuth();

    // Add event listener to detect storage changes (like logout from another tab)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'token' && e.newValue === null) {
        // Token was removed (logged out), redirect to sign in
        router.replace('/auth/sign-in');
      }
    };

    window.addEventListener('storage', handleStorageChange);

    // Clean up the event listener
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [router]);

  // Show loading state while checking authentication
  if (loading) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner label="Checking authentication..." />
      </div>
    );
  }

  // If authenticated, render the protected content
  if (isAuth) {
    return <>{children}</>;
  }

  // If not authenticated and not loading, return nothing (router.push should handle redirect)
  return null;
}
