type DoctorResultProps = {
  deck: {
    id: number;
    name: string;
    archetype: string;
    playStyle: string;
    format: string;
  };
  diagnosis: {
    summary: string;
    strengths: string[];
    risks: string[];
    suggestions: string[];
  };
};

import { DoctorRisks } from "./doctor-risks";
import { DoctorStrengths } from "./doctor-strengths";
import { DoctorSuggestions } from "./doctor-suggestions";
import { DoctorSummary } from "./doctor-summary";

export function DoctorResult({ deck, diagnosis }: DoctorResultProps) {
  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
        <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
          Deck Doctor
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white">{deck.name}</h1>

        <p className="mt-2 text-sm text-zinc-400">
          {deck.archetype} • {deck.playStyle} • {deck.format}
        </p>
      </section>

      <DoctorSummary summary={diagnosis.summary} />

      <div className="grid gap-6 lg:grid-cols-2">
        <DoctorStrengths items={diagnosis.strengths} />
        <DoctorRisks items={diagnosis.risks} />
      </div>

      <DoctorSuggestions items={diagnosis.suggestions} />
    </div>
  );
}