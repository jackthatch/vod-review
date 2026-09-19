import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "vod-review",
  description: "AI VOD review for League of Legends — find the moments that decided your games.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
