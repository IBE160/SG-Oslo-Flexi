const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function registerUser(email: string, password: string): Promise<any> {
  const response = await fetch(`${API_URL}/api/v1/users/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error?.message || 'Registration failed');
  }

  return data.data;
}
