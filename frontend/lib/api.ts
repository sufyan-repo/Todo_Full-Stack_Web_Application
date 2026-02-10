import { Todo, CreateTodoRequest, UpdateTodoRequest } from './types';

// Base API client with JWT handling that uses alternative request method
class ApiClient {
  private getBaseUrl(): string {
    if (typeof window !== 'undefined') {
      // Client-side: use NEXT_PUBLIC_API_URL from environment
      return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';  // Changed to match backend port
    } else {
      // Server-side: use NEXT_PUBLIC_API_URL from environment
      return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';  // Changed to match backend port
    }
  }

  private baseUrl: string;

  constructor() {
    this.baseUrl = this.getBaseUrl();
    console.log('API Client initialized with URL:', this.baseUrl);
  }

  // Get JWT token from storage
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  // Check if token is expired
  private isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  }

  // Prepare headers with JWT token
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    const token = this.getToken();
    if (token && !this.isTokenExpired(token)) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Robust request method using fetch with enhanced error handling and proxy support
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // Use proxy for client-side requests to avoid CORS issues
    let url: string;
    if (typeof window !== 'undefined') {
      // Client-side: route through Next.js proxy API
      url = `/api/proxy${endpoint}`;
    } else {
      // Server-side: direct backend access
      url = `${this.getBaseUrl()}${endpoint}`;
    }

    // Use fetch with enhanced CORS settings
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
      credentials: 'include', // Important for CORS requests with credentials
      mode: 'cors', // Explicitly set CORS mode
      cache: 'no-cache', // Prevent caching issues
      redirect: 'follow', // Follow redirects
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        this.handleTokenExpiration();
        throw new Error('Authentication required');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `API request failed: ${response.status}`);
      }

      // No Content (204) responses have no body
      if (response.status === 204) {
        return {} as unknown as T;
      }

      const text = await response.text();
      if (!text) return {} as unknown as T;
      return JSON.parse(text) as T;
    } catch (error) {
      console.error('Fetch failed - URL:', url, error);

      // Check if it's a network error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Try to determine the specific cause
        if (error.message.includes('CORS')) {
          throw new Error('CORS error: Cross-Origin request blocked. Please check backend CORS configuration.');
        } else if (error.message.includes('network') || error.message.includes('failed')) {
          // Verify if the server is actually running by making a simple test
          try {
            // This is just to check if the server is accessible
            await fetch(`${this.getBaseUrl()}/health`, { method: 'GET' });
            // If health check passes, there might be an issue with this specific endpoint
            throw new Error('Network error: Unable to connect to the specific API endpoint. The server appears to be running.');
          } catch (healthError) {
            throw new Error('Network error: Unable to connect to the server. Please check if the backend is running and accessible.');
          }
        } else {
          throw new Error(`Network error: ${error.message}`);
        }
      }

      throw error;
    }
  }


  // Handle token expiration
  private handleTokenExpiration(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user_name');
      window.location.replace('/auth/sign-in'); // Use replace to avoid back button issues
    }
  }

  // Auth methods
  async signIn(email: string, password: string): Promise<{ user: any; token: string }> {
    // Use the proxy for consistency with other API calls
    const url = typeof window !== 'undefined' ? `/api/proxy/api/auth/sign-in` : `${this.getBaseUrl()}/api/auth/sign-in`;

    // Use XMLHttpRequest directly to bypass Chrome extension interference
    if (typeof window !== 'undefined') {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText);
              // Store token and user name in localStorage
              localStorage.setItem('token', data.token);
              if (data.user?.full_name) {
                localStorage.setItem('user_name', data.user.full_name);
              } else if (data.user?.name) {
                localStorage.setItem('user_name', data.user.name);
              }
              resolve(data);
            } catch (e) {
              reject(new Error('Failed to parse response'));
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText);
              reject(new Error(errorData.detail || errorData.message || 'Sign in failed'));
            } catch (e) {
              reject(new Error('Sign in failed'));
            }
          }
        };

        xhr.onerror = function () {
          reject(new Error('Network error occurred'));
        };

        xhr.send(JSON.stringify({ email, password }));
      });
    }

    // Server-side fallback (shouldn't normally be called)
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || 'Sign in failed');
    }

    return await response.json();
  }

  async signUp(email: string, password: string, name: string): Promise<{ user: any; token: string }> {
    // Use the proxy for consistency with other API calls
    const url = typeof window !== 'undefined' ? `/api/proxy/api/auth/sign-up` : `${this.getBaseUrl()}/api/auth/sign-up`;

    // Use XMLHttpRequest directly to bypass Chrome extension interference
    if (typeof window !== 'undefined') {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText);
              // Store token and user name in localStorage
              localStorage.setItem('token', data.token);
              if (data.user?.full_name) {
                localStorage.setItem('user_name', data.user.full_name);
              } else if (data.user?.name) {
                localStorage.setItem('user_name', data.user.name);
              } else if (name) {
                localStorage.setItem('user_name', name);
              }
              resolve(data);
            } catch (e) {
              reject(new Error('Failed to parse response'));
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText);
              reject(new Error(errorData.detail || errorData.message || 'Sign up failed'));
            } catch (e) {
              reject(new Error('Sign up failed'));
            }
          }
        };

        xhr.onerror = function () {
          reject(new Error('Network error occurred'));
        };

        xhr.send(JSON.stringify({ email, password, name }));
      });
    }

    // Server-side fallback (shouldn't normally be called)
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || 'Sign up failed');
    }

    return await response.json();
  }

  async signOut(): Promise<void> {
    // Use the proxy for consistency with other API calls
    try {
      const url = typeof window !== 'undefined' ? `/api/proxy/api/auth/logout` : `${this.getBaseUrl()}/api/auth/logout`;
      await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.getHeaders(),
        },
      });
    } catch (error) {
      console.error('Logout API call failed:', error);
      // Continue with local cleanup even if API call fails
    }

    // Remove token from localStorage immediately to prevent any further API calls
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user_name');
    }

    // Redirect to login page after logout
    if (typeof window !== 'undefined') {
      window.location.href = '/auth/sign-in';
    }
  }

  // Todo methods using the simplified fetch approach
  async getTodos(): Promise<Todo[]> {
    const todos = await this.request<any[]>('/api/tasks/');
    return todos.map(this.mapTaskToTodo);
  }

  async createTodo(todoData: CreateTodoRequest): Promise<Todo> {
    const task = await this.request<any>('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
    return this.mapTaskToTodo(task);
  }

  async updateTodo(id: number, todoData: UpdateTodoRequest): Promise<Todo> {
    const task = await this.request<any>(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
    return this.mapTaskToTodo(task);
  }

  async deleteTodo(id: number): Promise<void> {
    await this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTodoComplete(id: number, completed: boolean): Promise<Todo> {
    const task = await this.request<any>(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
    return this.mapTaskToTodo(task);
  }

  private mapTaskToTodo(task: any): Todo {
    return {
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.completed,
      createdAt: task.created_at,
      updatedAt: task.updated_at,
      userId: task.user_id,
    };
  }
}

// Create a singleton instance
export const apiClient = new ApiClient();

// Export individual methods for convenience
export const signIn = apiClient.signIn.bind(apiClient);
export const signUp = apiClient.signUp.bind(apiClient);
export const signOut = apiClient.signOut.bind(apiClient);
export const getTodos = apiClient.getTodos.bind(apiClient);
export const createTodo = apiClient.createTodo.bind(apiClient);
export const updateTodo = apiClient.updateTodo.bind(apiClient);
export const deleteTodo = apiClient.deleteTodo.bind(apiClient);
export const toggleTodoComplete = apiClient.toggleTodoComplete.bind(apiClient);