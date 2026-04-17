"use client";

import { useState } from "react";
import { DeckCardPreview } from "./deck-card-preview";
import { DeckSection } from "./deck-section";

type DeckCard = {
  name: string;
  copies: number;
  imageSmallUrl?: string;
  imageUrl?: string;
  description?: string;
};

const mockDeck = {
  name: "Branded Consistente Local",
  archetype: "Branded",
  playStyle: "Consistente",
  winCondition:
    "Estabelecer pressão com fusões e manter follow-up para os próximos turnos.",
  howToPilot:
    "Priorize starters consistentes e preserve recursos importantes para o turno 2.",
  main: [
    {
      name: "Fallen of Albaz",
      copies: 2,
      imageSmallUrl:
        "https://images.ygoprodeck.com/images/cards_small/68468459.jpg",
      imageUrl: "https://images.ygoprodeck.com/images/cards/68468459.jpg",
      description:
        'If this card is Normal or Special Summoned: You can discard 1 card; Fusion Summon 1 Fusion Monster from your Extra Deck, using monsters from either field as material, including this card, but you cannot use other monsters you control as Fusion Material. You can only use this effect of "Fallen of Albaz" once per turn.',
    },
    {
      name: "Branded Fusion",
      copies: 3,
      imageSmallUrl:
        "https://images.ygoprodeck.com/images/cards_small/44362883.jpg",
      imageUrl: "https://images.ygoprodeck.com/images/cards/44362883.jpg",
      description:
        'Fusion Summon 1 Fusion Monster that mentions "Fallen of Albaz" as material from your Extra Deck, using 2 monsters from your hand, Deck, or field as Fusion Material.',
    },
  ],
  extra: [
    {
      name: "Albion the Branded Dragon",
      copies: 1,
      imageSmallUrl:
        "https://images.ygoprodeck.com/images/cards_small/38524592.jpg",
      imageUrl: "https://images.ygoprodeck.com/images/cards/38524592.jpg",
      description:
        'Fallen of Albaz + 1 LIGHT monster. If this card is Fusion Summoned: You can Fusion Summon 1 Level 8 or lower Fusion Monster from your Extra Deck, except "Albion the Branded Dragon", by banishing Fusion Materials listed on it from your field, GY, and/or face-up banished cards.',
    },
  ],
  side: [],
};

export function DeckViewer() {
  const [selectedCard, setSelectedCard] = useState<DeckCard | null>(null);

  return (
    <div className="relative flex h-[80vh] flex-col rounded-2xl border border-zinc-800 bg-zinc-900">
      <div className="border-b border-zinc-800 p-4">
        <h2 className="text-lg font-semibold">{mockDeck.name}</h2>
        <p className="text-sm text-zinc-400">
          {mockDeck.archetype} • {mockDeck.playStyle}
        </p>
      </div>

      <div className="deck-scroll flex-1 overflow-y-auto p-4">
        <div className="mb-6 space-y-3 rounded-2xl bg-zinc-950 p-4">
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">
              Condição de vitória
            </h3>
            <p className="mt-1 text-sm text-zinc-400">
              {mockDeck.winCondition}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-zinc-200">
              Como pilotar
            </h3>
            <p className="mt-1 text-sm text-zinc-400">
              {mockDeck.howToPilot}
            </p>
          </div>
        </div>

        <div className="space-y-6">
          <DeckSection
            title="Main Deck"
            cards={mockDeck.main}
            onSelectCard={setSelectedCard}
          />
          <DeckSection
            title="Extra Deck"
            cards={mockDeck.extra}
            onSelectCard={setSelectedCard}
          />
          <DeckSection
            title="Side Deck"
            cards={mockDeck.side}
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