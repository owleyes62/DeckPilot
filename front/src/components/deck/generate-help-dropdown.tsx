"use client";

import { useState } from "react";

export function GenerateHelpDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex w-full items-center justify-between px-4 py-4 text-left"
      >
        <div>
          <h2 className="text-sm font-semibold text-white">
            Como usar o chat para gerar decks
          </h2>
          <p className="mt-1 text-xs text-zinc-400">
            Dicas rápidas para obter resultados melhores neste MVP
          </p>
        </div>

        <span
          className={`text-sm text-zinc-400 transition-transform duration-200 ${
            isOpen ? "rotate-180" : "rotate-0"
          }`}
        >
          ▼
        </span>
      </button>

      {isOpen && (
        <div className="border-t border-zinc-800 px-4 py-4 text-sm text-zinc-300">
          <div className="space-y-5">
            <section>
              <h3 className="font-semibold text-white">1. Seja direto no pedido</h3>
              <p className="mt-2 text-zinc-400">
                O sistema funciona melhor quando você informa claramente o arquétipo
                ou o tipo de deck desejado.
              </p>

              <div className="mt-3 rounded-xl bg-zinc-950 p-3 text-zinc-300">
                <p>Exemplos:</p>
                <ul className="mt-2 list-disc space-y-1 pl-5">
                  <li>Quero um deck Branded consistente para torneio local.</li>
                  <li>Monte um deck Traptrix fácil de pilotar.</li>
                  <li>Quero um deck Swordsoul mais agressivo.</li>
                </ul>
              </div>
            </section>

            <section>
              <h3 className="font-semibold text-white">2. Refine na mesma conversa</h3>
              <p className="mt-2 text-zinc-400">
                Depois que a IA gerar um deck, prefira continuar na mesma sessão para
                pedir ajustes.
              </p>

              <div className="mt-3 rounded-xl bg-zinc-950 p-3 text-zinc-300">
                <p>Exemplos:</p>
                <ul className="mt-2 list-disc space-y-1 pl-5">
                  <li>Agora deixa esse deck mais barato.</li>
                  <li>Quero uma versão mais consistente.</li>
                  <li>Me passe uma lista mais agressiva.</li>
                  <li>Agora me mostre uma versão mais simples de pilotar.</li>
                </ul>
              </div>
            </section>

            <section>
              <h3 className="font-semibold text-white">3. O MVP ainda tem limitações</h3>
              <p className="mt-2 text-zinc-400">
                A IA ainda pode montar listas imperfeitas, incompletas ou com cartas
                incoerentes. O foco atual do sistema é validar o fluxo de geração e
                avaliação, não garantir listas competitivas perfeitas.
              </p>
            </section>

            <section>
              <h3 className="font-semibold text-white">4. Como obter resultados melhores</h3>
              <ul className="mt-2 list-disc space-y-2 pl-5 text-zinc-400">
                <li>Informe o arquétipo sempre que possível.</li>
                <li>Diga o objetivo: casual, torneio local, consistência, budget, etc.</li>
                <li>Peça mudanças curtas e específicas.</li>
                <li>Evite pedidos muito vagos ou muito amplos.</li>
              </ul>
            </section>

            <section>
              <h3 className="font-semibold text-white">5. Avaliação do deck</h3>
              <p className="mt-2 text-zinc-400">
                Mesmo quando a lista não estiver perfeita, você pode usar o Deck Doctor
                para receber um diagnóstico sobre coerência, riscos e possíveis melhorias.
              </p>
            </section>
          </div>
        </div>
      )}
    </div>
  );
}