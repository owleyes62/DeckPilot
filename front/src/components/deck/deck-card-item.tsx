"use client";

import { useState } from "react";
import { DeckCardPreview } from "./deck-card-preview";

type DeckCardItemProps = {
  name: string;
  copies: number;
  imageSmallUrl?: string;
  imageUrl?: string;
  description?: string;
  onOpenPreview: () => void;
};

export function DeckCardItem({
  name,
  copies,
  imageSmallUrl,
  onOpenPreview,
}: DeckCardItemProps) {
  return (
    <button
      type="button"
      onClick={onOpenPreview}
      className="flex w-full items-center justify-between rounded-xl bg-zinc-950 px-3 py-3 text-left transition hover:bg-zinc-900"
    >
      <div className="flex min-w-0 items-center gap-3">
        <div className="h-16 w-12 flex-shrink-0 overflow-hidden rounded-md border border-zinc-800 bg-zinc-900">
          {imageSmallUrl ? (
            <img
              src={imageSmallUrl}
              alt={name}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-[10px] text-zinc-500">
              Sem imagem
            </div>
          )}
        </div>

        <span className="truncate text-sm text-zinc-200">{name}</span>
      </div>

      <span className="ml-3 rounded-md bg-zinc-800 px-2 py-1 text-xs text-zinc-400">
        x{copies}
      </span>
    </button>
  );
}