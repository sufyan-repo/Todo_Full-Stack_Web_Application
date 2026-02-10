'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

/**
 * Theme type definition
 * - 'light': Explicit light theme preference
 * - 'dark': Explicit dark theme preference
 * - 'system': Follow system preference
 */
export type Theme = 'light' | 'dark' | 'system';

/**
 * Theme context interface
 * Provides theme state and setter function
 */
interface ThemeContextType {
  /** Current resolved theme ('light' or 'dark') */
  theme: 'light' | 'dark';
  /** Set theme preference ('light', 'dark', or 'system') */
  setTheme: (theme: Theme) => void;
}

/**
 * Theme context for global theme state management
 */
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

/**
 * ThemeProvider component properties
 */
interface ThemeProviderProps {
  children: ReactNode;
}

/**
 * ThemeProvider - Client component that manages theme state
 *
 * Theme detection priority:
 * 1. localStorage saved preference (if exists)
 * 2. System preference (prefers-color-scheme)
 * 3. Fallback to 'light'
 *
 * @param props - Component props
 * @returns Theme context provider
 */
export function ThemeProvider({ children }: ThemeProviderProps) {
  const [theme, setThemeState] = useState<'light' | 'dark'>(() => {
    // Initialize state with a default that matches what the server would render
    if (typeof window !== 'undefined') {
      // On client, try to determine the theme based on system preference
      const stored = localStorage.getItem('theme') as Theme | null;
      const system = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      return stored === 'system' ? system : (stored || system);
    }
    // On server, default to light theme
    return 'light';
  });

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;

    // Priority 1: Check localStorage for saved preference
    const stored = localStorage.getItem('theme') as Theme | null;

    // Priority 2: Get system preference
    const system = window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';

    // Resolve theme: stored → system → fallback
    const resolved = stored === 'system' ? system : (stored || system);

    setThemeState(resolved);

    // Mark as mounted to prevent server/client mismatch
    setMounted(true);

    // Apply dark class to html element for Tailwind dark mode
    document.documentElement.classList.toggle('dark', resolved === 'dark');
  }, []);

  /**
   * Set theme preference and persist to localStorage
   * @param newTheme - Theme preference to set
   */
  const setTheme = (newTheme: Theme) => {
    // Save to localStorage for persistence across sessions
    localStorage.setItem('theme', newTheme);

    // Resolve final theme
    const resolved =
      newTheme === 'system'
        ? window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light'
        : newTheme;

    setThemeState(resolved);

    // Apply to DOM for Tailwind dark mode
    document.documentElement.classList.toggle('dark', resolved === 'dark');
  };

  // Apply theme to document element when theme changes (only after mounted)
  useEffect(() => {
    if (!mounted) return;
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme, mounted]);

  // Only provide the theme context after mounting to prevent hydration issues
  const contextValue = mounted
    ? { theme, setTheme }
    : { theme: 'light', setTheme }; // Provide a default during hydration

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

/**
 * useTheme hook
 *
 * Provides access to theme state and setter function
 *
 * @example
 * ```tsx
 * const { theme, setTheme } = useTheme();
 * console.log(theme); // 'light' | 'dark'
 * setTheme('dark'); // Switch to dark mode
 * ```
 *
 * @throws Error if used outside ThemeProvider
 * @returns Theme context value
 */
export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);

  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }

  return context;
}