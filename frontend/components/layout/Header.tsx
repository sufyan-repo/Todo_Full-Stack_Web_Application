"use client";

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ThemeToggle } from '@/components/ui/ThemeToggle';
import { UserMenu } from '@/components/ui/UserMenu';
import { cn } from '@/lib/utils';
import { Layout, CheckCircle2 } from 'lucide-react';

import { useAuth } from '@/hooks/useAuth';

export default function Header() {
  const pathname = usePathname();
  const { isAuthenticated, isLoading } = useAuth();

  // Don't hide header on auth pages anymore
  return (
    <header
      className={cn(
        'sticky top-0 z-50 glass w-full',
        'border-b border-ui-border/20',
        'transition-all duration-500 ease-in-out',
        'backdrop-blur-xl bg-background/60'
      )}
    >
      <div className="section-horizontal py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-3 transition-all duration-300 hover:scale-105 active:scale-95 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary text-white shadow-lg shadow-primary/30 group-hover:shadow-primary/50 group-hover:rotate-6 transition-all duration-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 12l2 2 4-4" />
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                </svg>
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-foreground leading-none">
                Todo<span className="text-primary">List</span>
              </h1>
            </Link>

            {/* Main Nav */}
            <nav className="hidden md:flex items-center gap-1">
              <Link
                href="/"
                className={cn(
                  "px-4 py-2 text-sm font-bold rounded-xl transition-all duration-300",
                  pathname === '/' ? "bg-primary/10 text-primary" : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
              >
                Home
              </Link>
              {!isLoading && isAuthenticated && (
                <Link
                  href="/dashboard"
                  className={cn(
                    "px-4 py-2 text-sm font-bold rounded-xl transition-all duration-300",
                    pathname === '/dashboard' ? "bg-primary/10 text-primary" : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  Dashboard
                </Link>
              )}
            </nav>
          </div>

          <div className="flex items-center gap-4">
            {/* Login button for unauthenticated users */}
            {!isLoading && !isAuthenticated && (
              <Link href="/auth/sign-in">
                <button className="px-4 py-2 text-sm font-bold rounded-xl transition-all duration-300 text-muted-foreground hover:text-foreground hover:bg-muted">
                  Login
                </button>
              </Link>
            )}

            <div className="flex items-center gap-2 p-1.5 rounded-[1.25rem] bg-muted/30 border border-ui-border/20 shadow-inner">
              <ThemeToggle position="header" />
              <div className="w-px h-5 bg-ui-border/30 mx-1" />
              <UserMenu />
            </div>

            {!pathname?.includes('/dashboard') && !isLoading && isAuthenticated && (
              <Link href="/dashboard" className="hidden sm:block">
                <button className="px-5 py-2.5 bg-foreground text-background text-sm font-black rounded-xl hover:opacity-90 transition-all active:scale-95 shadow-lg shadow-foreground/10">
                  Go to Workspace
                </button>
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
