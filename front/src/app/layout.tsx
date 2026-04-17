import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "DeckPilot",
  description: "Seu copiloto de IA para montar e avaliar decks de Yu-Gi-Oh!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-zinc-950 text-zinc-100 antialiased">
        <div className="min-h-screen">
          <header className="sticky top-0 z-40 border-b border-zinc-800 bg-zinc-950/90 backdrop-blur">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
              <Link href="/" className="text-lg font-bold tracking-tight text-white">
                DeckPilot
              </Link>

              <nav className="flex items-center gap-2 text-sm">
                <Link
                  href="/generate"
                  className="rounded-lg px-3 py-2 text-zinc-300 transition hover:bg-zinc-800 hover:text-white"
                >
                  Gerar Deck
                </Link>

                <Link
                  href="/evaluate/1"
                  className="rounded-lg px-3 py-2 text-zinc-300 transition hover:bg-zinc-800 hover:text-white"
                >
                  Avaliar Deck
                </Link>
              </nav>
            </div>
          </header>

          {children}
        </div>
      </body>
    </html>
  );
}