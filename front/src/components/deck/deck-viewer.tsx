import { DeckSection } from "./deck-section";

const mockDeck = {
  name: "Branded Consistente Local",
  archetype: "Branded",
  playStyle: "Consistente",
  winCondition:
    "Estabelecer pressão com fusões e manter follow-up para os próximos turnos.",
  howToPilot:
    "Priorize starters consistentes e preserve recursos importantes para o turno 2.",
  main: [
    { name: "Fallen of Albaz", copies: 2 },
    { name: "Branded Fusion", copies: 3 },
  ],
  extra: [
    { name: "Albion the Branded Dragon", copies: 1 },
  ],
  side: [],
};

export function DeckViewer() {
  return (
    <div className="flex h-[80vh] flex-col rounded-2xl border border-zinc-800 bg-zinc-900">
      <div className="border-b border-zinc-800 p-4">
        <h2 className="text-lg font-semibold">{mockDeck.name}</h2>
        <p className="text-sm text-zinc-400">
          {mockDeck.archetype} • {mockDeck.playStyle}
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
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
          <DeckSection title="Main Deck" cards={mockDeck.main} />
          <DeckSection title="Extra Deck" cards={mockDeck.extra} />
          <DeckSection title="Side Deck" cards={mockDeck.side} />
        </div>
      </div>
    </div>
  );
}