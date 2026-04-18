"use client";

import { useState } from "react";
import { ChatContainer } from "@/components/chat/chat-container";
import { DeckViewer } from "@/components/deck/deck-viewer";
import { GenerateHelpDropdown } from "@/components/deck/generate-help-dropdown";
import type { ChatSavedDeckDetail } from "@/features/chat/types/chat.types";

export default function GeneratePage() {
  const [deck, setDeck] = useState<ChatSavedDeckDetail | null>(null);

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 p-6 lg:flex-row">
        <section className="w-full lg:w-[45%]">
          <ChatContainer onDeckChange={setDeck} />
        </section>

        <section className="flex w-full flex-col gap-4 lg:w-[55%]">
          <GenerateHelpDropdown/>
          <div id="deck-viewer">
            <DeckViewer deck={deck} />
          </div>
        </section>
      </div>
    </main>
  );
}