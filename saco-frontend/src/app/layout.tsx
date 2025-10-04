import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SACO AI ASSISTANT",
  description: "Intelligent Location Analysis & Amenity Discovery - Powered by SACO Consulting",
  icons: {
    icon: [
      { url: '/icon.ico', sizes: 'any' },
      { url: '/icon.ico', sizes: '32x32', type: 'image/x-icon' },
      { url: '/icon.ico', sizes: '16x16', type: 'image/x-icon' }
    ],
    apple: '/icon.ico',
    shortcut: '/icon.ico',
  },
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/icon.ico" sizes="any" />
        <link rel="shortcut icon" href="/icon.ico" />
        <link rel="apple-touch-icon" href="/icon.ico" />
        <meta name="theme-color" content="#000000" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
