type DoctorStrengthsProps = {
  items: string[];
};

export function DoctorStrengths({ items }: DoctorStrengthsProps) {
  return (
    <section className="rounded-2xl border border-emerald-900 bg-emerald-950/20 p-6">
      <h2 className="text-lg font-semibold text-emerald-300">Pontos fortes</h2>

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