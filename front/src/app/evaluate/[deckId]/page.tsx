"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { DoctorResult } from "@/components/doctor/doctor-result";
import { getDoctorAnalysis } from "@/features/doctor/api/doctor-api";
import type { DoctorDeck } from "@/features/doctor/types/doctor.types";

export default function EvaluateDeckPage() {
  const params = useParams<{ deckId: string }>();
  const rawDeckId = params?.deckId;

  const deckId = useMemo(() => {
    if (!rawDeckId) return NaN;
    return Number(rawDeckId);
  }, [rawDeckId]);

  const [analysis, setAnalysis] = useState<DoctorDeck | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadAnalysis() {
      try {
        setIsLoading(true);
        setError(null);

        const response = await getDoctorAnalysis(deckId);
        setAnalysis(response);
      } catch {
        setError("Não foi possível carregar a avaliação do deck.");
      } finally {
        setIsLoading(false);
      }
    }

    if (Number.isNaN(deckId)) {
      setError("ID de deck inválido.");
      setIsLoading(false);
      return;
    }

    loadAnalysis();
  }, [deckId]);

  if (isLoading) {
    return (
      <main className="min-h-screen bg-zinc-950 text-zinc-100">
        <div className="mx-auto max-w-6xl p-6">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 text-sm text-zinc-400">
            Carregando avaliação do deck...
          </div>
        </div>
      </main>
    );
  }

  if (error || !analysis) {
    return (
      <main className="min-h-screen bg-zinc-950 text-zinc-100">
        <div className="mx-auto max-w-6xl p-6">
          <div className="rounded-2xl border border-red-900 bg-red-950/20 p-6 text-sm text-red-300">
            {error ?? "Não foi possível carregar a avaliação."}
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto max-w-6xl p-6">
        <DoctorResult
          deck={{
            id: analysis.deck_id,
            name: `Deck #${analysis.deck_id}`,
            archetype: "Deck avaliado",
            playStyle: "Diagnóstico automático",
            format: "TCG",
          }}
          diagnosis={{
            summary: analysis.summary,
            strengths: analysis.strengths,
            risks: analysis.risks,
            suggestions: analysis.suggestions,
          }}
        />
      </div>
    </main>
  );
}