type DeckCardPreviewProps = {
  name: string;
  imageUrl?: string;
  description?: string;
  onClose: () => void;
};

export function DeckCardPreview({
  name,
  imageUrl,
  description,
  onClose,
}: DeckCardPreviewProps) {
  return (
    <div
      className="absolute inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={onClose}
    >
      <div
        className="relative max-h-[90%] w-full max-w-3xl overflow-hidden rounded-2xl border border-zinc-700 bg-zinc-950 shadow-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          onClick={onClose}
          className="absolute right-3 top-3 z-10 rounded-lg bg-zinc-900 px-3 py-2 text-xs text-zinc-300 transition hover:bg-zinc-800 hover:text-white"
        >
          Fechar
        </button>

        <div className="grid max-h-[90vh] grid-cols-1 overflow-y-auto md:grid-cols-[320px_1fr]">
          <div className="flex items-start justify-center bg-zinc-900 p-6">
            <div className="w-full max-w-[260px] overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950">
              {imageUrl ? (
                <img
                  src={imageUrl}
                  alt={name}
                  className="h-auto w-full object-cover"
                />
              ) : (
                <div className="flex h-[360px] items-center justify-center px-4 text-center text-sm text-zinc-500">
                  Imagem não disponível
                </div>
              )}
            </div>
          </div>

          <div className="p-6">
            <h3 className="text-xl font-semibold text-white">{name}</h3>

            <div className="mt-6">
              <h4 className="text-sm font-semibold uppercase tracking-wide text-zinc-400">
                Efeito / descrição
              </h4>
              <div className="mt-3 rounded-xl bg-zinc-900 p-4">
                <p className="whitespace-pre-wrap text-sm leading-7 text-zinc-300">
                  {description || "Descrição não disponível."}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}