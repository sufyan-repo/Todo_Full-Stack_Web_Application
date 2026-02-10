'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, getToken, removeToken } from '@/lib/auth';

export const useAuth = () => {
  const [isAuthenticatedState, setIsAuthenticated] = useState<boolean | null>(null); // null means loading
  const router = useRouter();

  useEffect(() => {
    // Check authentication status immediately
    const checkAuthStatus = () => {
      const authStatus = isAuthenticated();
      setIsAuthenticated(authStatus);
    };

    // Check initially
    checkAuthStatus();

    // Listen for storage changes (e.g., logout from another tab)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'token') {
        const authStatus = isAuthenticated();
        setIsAuthenticated(authStatus);
      }
    };

    window.addEventListener('storage', handleStorageChange);

    // Cleanup listener
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const logout = () => {
    // Remove token from localStorage
    removeToken();
    
    // Update state
    setIsAuthenticated(false);
    
    // Redirect to login
    router.push('/auth/sign-in');
  };

  return {
    isAuthenticated: isAuthenticatedState,
    isLoading: isAuthenticatedState === null,
    logout,
  };
};