"use client";

import { useMemo, useState } from "react";
import type { ChatSavedDeckDetail } from "@/features/chat/types/chat.types";
import { DeckCardPreview } from "./deck-card-preview";
import { DeckSection } from "./deck-section";

type DeckCard = {
  name: string;
  copies: number;
  imageSmallUrl?: string;
  imageUrl?: string;
  description?: string;
};

type DeckViewerProps = {
  deck?: ChatSavedDeckDetail | null;
};

export function DeckViewer({ deck }: DeckViewerProps) {
  const [selectedCard, setSelectedCard] = useState<DeckCard | null>(null);

  const parsedDeck = useMemo(() => {
    if (!deck) return null;

    const main = deck.deck_cards
      .filter((item) => item.section === "main")
      .map((item) => ({
        name: item.card.name,
        copies: item.copies,
        imageSmallUrl: item.card.image_small_url ?? undefined,
        imageUrl: item.card.image_url ?? undefined,
        description: item.card.description ?? undefined,
      }));

    const extra = deck.deck_cards
      .filter((item) => item.section === "extra")
      .map((item) => ({
        name: item.card.name,
        copies: item.copies,
        imageSmallUrl: item.card.image_small_url ?? undefined,
        imageUrl: item.card.image_url ?? undefined,
        description: item.card.description ?? undefined,
      }));

    const side = deck.deck_cards
      .filter((item) => item.section === "side")
      .map((item) => ({
        name: item.card.name,
        copies: item.copies,
        imageSmallUrl: item.card.image_small_url ?? undefined,
        imageUrl: item.card.image_url ?? undefined,
        description: item.card.description ?? undefined,
      }));

    return {
      name: deck.name,
      archetype: deck.archetype,
      playStyle: deck.play_style,
      winCondition: deck.win_condition ?? "Não informado.",
      howToPilot: deck.how_to_pilot ?? "Não informado.",
      main,
      extra,
      side,
    };
  }, [deck]);

  if (!parsedDeck) {
    return (
      <div className="flex h-[80vh] items-center justify-center rounded-2xl border border-zinc-800 bg-zinc-900 p-6 text-center text-sm text-zinc-500">
        O deck gerado aparecerá aqui quando a IA salvar uma versão válida.
      </div>
    );
  }

  return (
    <div className="relative flex h-[80vh] flex-col rounded-2xl border border-zinc-800 bg-zinc-900">
      <div className="border-b border-zinc-800 p-4">
        <h2 className="text-lg font-semibold">{parsedDeck.name}</h2>
        <p className="text-sm text-zinc-400">
          {parsedDeck.archetype} • {parsedDeck.playStyle}
        </p>
      </div>

      <div className="deck-scroll flex-1 overflow-y-auto p-4">
        <div className="mb-6 space-y-3 rounded-2xl bg-zinc-950 p-4">
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">
              Condição de vitória
            </h3>
            <p className="mt-1 text-sm text-zinc-400">
              {parsedDeck.winCondition}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-zinc-200">
              Como pilotar
            </h3>
            <p className="mt-1 text-sm text-zinc-400">
              {parsedDeck.howToPilot}
            </p>
          </div>
        </div>

        <div className="space-y-6">
          <DeckSection
            title="Main Deck"
            cards={parsedDeck.main}
            onSelectCard={setSelectedCard}
          />
          <DeckSection
            title="Extra Deck"
            cards={parsedDeck.extra}
            onSelectCard={setSelectedCard}
          />
          <DeckSection
            title="Side Deck"
            cards={parsedDeck.side}
            onSelectCard={setSelectedCard}
          />
        </div>
      </div>

      {selectedCard && (
        <DeckCardPreview
          name={selectedCard.name}
          imageUrl={selectedCard.imageUrl}
          description={selectedCard.description}
          onClose={() => setSelectedCard(null)}
        />
      )}
    </div>
  );
}