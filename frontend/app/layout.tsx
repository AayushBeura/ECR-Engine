import { Roboto_Mono } from "next/font/google";
import "./globals.css";
import { Metadata } from "next";

const robotoMono = Roboto_Mono({
  variable: "--font-roboto-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Explainable Credit Engine",
  description: "AI-Driven Digital Lending Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${robotoMono.variable} antialiased min-h-screen bg-background font-mono text-foreground`}>
        {children}
      </body>
    </html>
  );
}
