"use client";

import { useState } from "react";

type ChatInputProps = {
  onSendMessage: (content: string) => Promise<void>;
  isLoading?: boolean;
};

export function ChatInput({
  onSendMessage,
  isLoading = false,
}: ChatInputProps) {
  const [value, setValue] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = value.trim();
    if (!trimmed || isLoading) return;

    setValue("");
    await onSendMessage(trimmed);
  }

  return (
    <form className="flex gap-3" onSubmit={handleSubmit}>
      <input
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ex: Quero um deck Branded consistente para torneio local"
        className="flex-1 rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="rounded-xl bg-blue-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isLoading ? "Enviando..." : "Enviar"}
      </button>
    </form>
  );
}