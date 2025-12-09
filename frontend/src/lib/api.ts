const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface UserResponse {
  id: string;
  email: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  detail?: string;
}

export const registerUser = async (data: any) => {
  const response = await fetch(`${API_URL}/api/v1/users/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error?.message || "Registration failed");
  }

  return response.json();
};

export const completeOnboarding = async (token: string) => {
  const response = await fetch(`${API_URL}/api/v1/users/onboarding`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to complete onboarding");
  }

  return response.json();
};

export async function login(username: string, password: string): Promise<AuthResponse> {
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
