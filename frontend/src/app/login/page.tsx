'use client';

import LoginForm from '@/components/LoginForm';

export default function LoginPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md">
        <LoginForm />
        <p className="mt-4 text-center text-gray-600">
          Don&apos;t have an account? <a href="/register" className="text-blue-700 underline hover:text-blue-800">Register</a>
        </p>
      </div>
    </div>
  );
}