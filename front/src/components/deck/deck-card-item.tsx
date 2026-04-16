type DeckCardItemProps = {
  name: string;
  copies: number;
};

export function DeckCardItem({ name, copies }: DeckCardItemProps) {
  return (
    <div className="flex items-center justify-between rounded-xl bg-zinc-950 px-4 py-3">
      <span className="text-sm text-zinc-200">{name}</span>
      <span className="rounded-md bg-zinc-800 px-2 py-1 text-xs text-zinc-400">
        x{copies}
      </span>
    </div>
  );
}