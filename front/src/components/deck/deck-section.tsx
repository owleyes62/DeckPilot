import { DeckCardItem } from "./deck-card-item";

type DeckCard = {
  name: string;
  copies: number;
  imageSmallUrl?: string;
  imageUrl?: string;
  description?: string;
};

type DeckSectionProps = {
  title: string;
  cards: DeckCard[];
  onSelectCard: (card: DeckCard) => void;
};

export function DeckSection({
  title,
  cards,
  onSelectCard,
}: DeckSectionProps) {
  const totalCopies = cards.reduce((acc, card) => acc + card.copies, 0);

  return (
    <section>
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-zinc-200">{title}</h3>
        <span className="text-xs text-zinc-500">{totalCopies} cartas</span>
      </div>

      <div className="space-y-2">
        {cards.length > 0 ? (
          cards.map((card) => (
            <DeckCardItem
              key={`${title}-${card.name}`}
              name={card.name}
              copies={card.copies}
              imageSmallUrl={card.imageSmallUrl}
              imageUrl={card.imageUrl}
              description={card.description}
              onOpenPreview={() => onSelectCard(card)}
            />
          ))
        ) : (
          <div className="rounded-xl border border-dashed border-zinc-700 p-4 text-sm text-zinc-500">
            Nenhuma carta nesta seção.
          </div>
        )}
      </div>
    </section>
  );
}