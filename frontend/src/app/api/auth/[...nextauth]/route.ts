import NextAuth, { NextAuthOptions } from "next-auth";
import GithubProvider from "next-auth/providers/github";

export const authOptions: NextAuthOptions = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID as string,
      clientSecret: process.env.GITHUB_SECRET as string,
    }),
  ],
  callbacks: {
    async jwt({ token, user, account }) {
      // When the user logs in, we can intercept the token to sync with our FastAPI backend
      // In a full production app, this is where you'd call the /sync-user backend route
      if (account && user) {
        // Call our FastAPI backend to sync the user and get our DB integer ID
        try {
          const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/sync-user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              id: user.id,
              email: user.email || '',
              name: user.name || 'Developer',
            }),
          });
          
          if (res.ok) {
            const data = await res.json();
            token.userId = data.user_id; // The integer ID from Postgres
          } else {
            token.userId = user.id; // Fallback
          }
        } catch (error) {
          console.error("Failed to sync user with backend", error);
          token.userId = user.id; // Fallback
        }
        
        token.accessToken = account.access_token;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        // @ts-ignore
        session.user.id = token.userId as string;
      }
      return session;
    },
  },
  pages: {
    signIn: '/login', // We will build this custom login page next
  },
  session: {
    strategy: "jwt",
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
