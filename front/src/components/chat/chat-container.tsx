"use client";

import { useEffect, useState } from "react";
import { createChatSession, sendChatMessage } from "@/features/chat/api/chat-api";
import type {
  ChatMessage,
  ChatSavedDeckDetail,
} from "@/features/chat/types/chat.types";
import { ChatInput } from "./chat-input";
import { ChatMessageList } from "./chat-message-list";

type ChatContainerProps = {
  onDeckChange: (deck: ChatSavedDeckDetail | null) => void;
};

export function ChatContainer({ onDeckChange }: ChatContainerProps) {
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function initializeSession() {
      const session = await createChatSession();
      setSessionId(session.id);

      setMessages([
        {
          id: 0,
          session_id: session.id,
          role: "assistant",
          content: "Olá! Me diga que tipo de deck você quer montar e eu te ajudo.",
          created_at: new Date().toISOString(),
        },
      ]);
    }

    initializeSession();
  }, []);

  async function handleSendMessage(content: string) {
    if (!sessionId) return;

    setIsLoading(true);

    try {
      const response = await sendChatMessage(sessionId, content);

      setMessages((prev) => [
        ...prev,
        response.user_message,
        response.assistant_message,
      ]);

      onDeckChange(response.saved_deck_detail ?? null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex h-[80vh] flex-col rounded-2xl border border-zinc-800 bg-zinc-900">
      <div className="border-b border-zinc-800 p-4">
        <h1 className="text-lg font-semibold">DeckPilot Chat</h1>
        <p className="text-sm text-zinc-400">
          Converse com a IA para gerar ou refinar um deck.
        </p>
      </div>

      <div className="flex-1 overflow-hidden">
        <ChatMessageList messages={messages} />
      </div>

      <div className="border-t border-zinc-800 p-4">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}