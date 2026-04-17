"use client";

import Link from "next/link";

type ChatGeneratedDeckCardProps = {
  savedDeck?: {
    id: number;
    name: string;
    archetype: string;
    play_style: string;
    format: string;
    source: string;
  } | null;
  generationStatus: {
    attempted: boolean;
    saved: boolean;
    message: string;
  };
  invalidCards: string[];
};

export function ChatGeneratedDeckCard({
  savedDeck,
  generationStatus,
  invalidCards,
}: ChatGeneratedDeckCardProps) {
  if (!generationStatus.attempted) {
    return null;
  }

  const statusLabel = generationStatus.saved
    ? "Deck salvo"
    : "Geração incompleta";

  const statusClasses = generationStatus.saved
    ? "border-emerald-800 bg-emerald-950/40 text-emerald-300"
    : "border-amber-800 bg-amber-950/40 text-amber-300";

  return (
    <div className="mt-3 rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
      <div className="flex flex-col gap-3">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
              Deck gerado
            </p>

            <h3 className="mt-1 text-base font-semibold text-white">
              {savedDeck?.name ?? "Deck não salvo"}
            </h3>

            {savedDeck && (
              <p className="mt-1 text-sm text-zinc-400">
                {savedDeck.archetype} • {savedDeck.play_style} •{" "}
                {savedDeck.format}
              </p>
            )}
          </div>

          <span
            className={`rounded-full border px-3 py-1 text-xs font-medium ${statusClasses}`}
          >
            {statusLabel}
          </span>
        </div>

        <div className="rounded-xl bg-zinc-950 p-3">
          <p className="text-sm text-zinc-300">{generationStatus.message}</p>
        </div>

        {invalidCards.length > 0 && (
          <div className="rounded-xl border border-amber-900 bg-amber-950/30 p-3">
            <p className="text-sm font-medium text-amber-300">
              Cartas não encontradas no catálogo
            </p>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-200">
              {invalidCards.map((cardName) => (
                <li key={cardName}>{cardName}</li>
              ))}
            </ul>
          </div>
        )}

        {savedDeck && (
          <div className="flex flex-wrap gap-2">
            <a
              href="#deck-viewer"
              className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-500"
            >
              Ver no painel
            </a>

            <Link
              href={`/evaluate/${savedDeck.id}`}
              className="rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-2 text-sm font-medium text-zinc-200 transition hover:bg-zinc-800"
            >
              Levar para avaliação
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}