import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-[calc(100vh-73px)] bg-zinc-950 text-zinc-100">
      <section className="mx-auto flex max-w-7xl flex-col px-6 py-20">
        <div className="max-w-3xl">
          <span className="mb-4 inline-flex rounded-full border border-zinc-800 bg-zinc-900 px-3 py-1 text-xs text-zinc-400">
            MVP • Geração e avaliação de decks com IA
          </span>

          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
            Monte, refine e avalie decks de Yu-Gi-Oh! com IA.
          </h1>

          <p className="mt-6 text-base leading-7 text-zinc-400 sm:text-lg">
            Converse com a IA para descobrir um deck ideal, gerar listas,
            refinar versões e depois avaliar o resultado com o Deck Doctor.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/generate"
              className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-blue-500"
            >
              Começar geração
            </Link>

            <Link
              href="/evaluate/1"
              className="inline-flex items-center justify-center rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-3 text-sm font-medium text-zinc-200 transition hover:bg-zinc-800"
            >
              Ver avaliação
            </Link>
          </div>
        </div>

        <div className="mt-16 grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <h2 className="text-sm font-semibold text-white">Chat de geração</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Converse com a IA para pedir um deck específico ou descobrir
              opções com base no seu perfil de jogo.
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <h2 className="text-sm font-semibold text-white">Refinamento por conversa</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Ajuste o deck ao longo da sessão com pedidos como mais
              consistência, menor custo ou estilo mais agressivo.
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <h2 className="text-sm font-semibold text-white">Deck Doctor</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Avalie o deck escolhido e receba diagnóstico, forças, riscos
              e sugestões de melhoria.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}