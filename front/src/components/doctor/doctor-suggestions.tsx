type DoctorSuggestionsProps = {
  items: string[];
};

export function DoctorSuggestions({ items }: DoctorSuggestionsProps) {
  return (
    <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
      <h2 className="text-lg font-semibold text-white">Sugestões de melhoria</h2>

      <ul className="mt-4 space-y-3">
        {items.map((item) => (
          <li
            key={item}
            className="rounded-xl bg-zinc-950 p-4 text-sm leading-6 text-zinc-300"
          >
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}