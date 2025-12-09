import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Extend the built-in types
declare module "next-auth" {
  interface User {
    accessToken?: string;
    is_onboarded?: boolean;
  }
  interface Session {
    accessToken?: string;
    user: {
      email?: string | null;
      is_onboarded?: boolean;
    }
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    is_onboarded?: boolean;
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) return null;

        const formData = new URLSearchParams();
        formData.append("username", credentials.username);
        formData.append("password", credentials.password);

        try {
          // 1. Get Token
          const res = await fetch(`${API_URL}/api/v1/login/access-token`, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData.toString(),
          });

          const data = await res.json();

          if (res.ok && data.access_token) {
            // 2. Get User Details (for is_onboarded)
            const userRes = await fetch(`${API_URL}/api/v1/users/me`, {
              method: "GET",
              headers: {
                "Authorization": `Bearer ${data.access_token}`,
              },
            });
            const userData = await userRes.json();

            // Return object to be stored in JWT
            return {
              id: userData.id || "user-id-placeholder",
              email: credentials.username,
              accessToken: data.access_token,
              is_onboarded: userData.is_onboarded ?? false,
            };
          }
          return null;
        } catch (e) {
          console.error("Login error:", e);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user, trigger, session }) {
      if (trigger === "update" && session?.user?.is_onboarded !== undefined) {
        token.is_onboarded = session.user.is_onboarded;
      }
      if (user) {
        token.accessToken = user.accessToken;
        token.email = user.email;
        token.is_onboarded = user.is_onboarded;
      }
      return token;
    },
    async session({ session, token }) {
      if (token && session.user) {
        session.accessToken = token.accessToken;
        session.user.email = token.email;
        session.user.is_onboarded = token.is_onboarded;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
