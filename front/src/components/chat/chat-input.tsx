export function ChatInput() {
  return (
    <form className="flex gap-3">
      <input
        type="text"
        placeholder="Ex: Quero um deck Branded consistente para torneio local"
        className="flex-1 rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
      />
      <button
        type="submit"
        className="rounded-xl bg-blue-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-blue-500"
      >
        Enviar
      </button>
    </form>
  );
}