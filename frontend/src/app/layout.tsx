import type { Metadata } from "next";
import "./globals.css";
import Providers from "../components/Providers";

export const metadata: Metadata = {
  title: "FlowMind — AI-Powered Developer Dashboard",
  description: "Unified intelligence dashboard that uses AI to prioritize your GitHub notifications and Gmail messages. Built with Next.js, FastAPI, and Gemini.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-full flex flex-col font-sans" style={{ fontFamily: "'Inter', sans-serif" }}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
