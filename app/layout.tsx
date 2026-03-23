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
  title: "이형주 | AI & Data Specialist",
  description: "RAG & 데이터 엔지니어 - 검색을 '되게'가 아니라 '맞게' 만드는 사람",
  metadataBase: new URL("https://portfolio-sigma-sepia-91.vercel.app"),
  openGraph: {
    url: "https://portfolio-sigma-sepia-91.vercel.app",
    title: "이형주 | AI & Data Specialist",
    description: "RAG & 데이터 엔지니어 - 검색을 '되게'가 아니라 '맞게' 만드는 사람",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
