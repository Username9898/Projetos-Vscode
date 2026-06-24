import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Dentarium AI Enterprise",
  description: "Plataforma SaaS de Inteligência Artificial Empresarial",
  author: "Roberto Ribeiro",
  keywords: ["IA", "dashboard", "automação", "odontologia", "CAD/CAM", "analytics"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body className={inter.className}>{children}</body>
    </html>
  );
}