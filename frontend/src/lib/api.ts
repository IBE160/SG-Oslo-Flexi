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

export async function login(username: string, password: string): Promise<any> {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/api/v1/login/access-token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Login failed');
  }

  // Store token in localStorage (simplest for MVP)
  localStorage.setItem('token', data.access_token);
  return data;
}
