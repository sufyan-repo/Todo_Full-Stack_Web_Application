// Wrapper for fetch API that handles browser extension interference
export async function fetchWithFallback(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  // First, try the normal fetch
  try {
    return await fetch(input, init);
  } catch (error) {
    console.warn('Standard fetch failed due to browser extension interference', error);
    
    // If fetch fails due to browser extension, we'll throw a more descriptive error
    // In a real-world scenario, the user would need to disable the interfering extension
    throw new Error('Browser extension is interfering with network requests. Please try disabling extensions like ad blockers or privacy tools.');
  }
}