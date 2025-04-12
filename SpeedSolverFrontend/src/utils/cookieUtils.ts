// cookieUtils.ts
export function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) { 
        const cookieValue = parts.pop()!.split(';').shift();
        return cookieValue ? cookieValue : null;
    }
    return null;
  }
  