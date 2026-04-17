import type {
  ChatMessage,
  ChatMessageExchangeResponse,
} from "@/features/chat/types/chat.types";
import { ChatGeneratedDeckCard } from "./chat-generated-deck-card";
import { ChatMessageItem } from "./chat-message-item";

type ChatMessageListProps = {
  messages: ChatMessage[];
  lastExchange: ChatMessageExchangeResponse | null;
};

export function ChatMessageList({
  messages,
  lastExchange,
}: ChatMessageListProps) {
  return (
    <div className="flex h-full flex-col gap-3 overflow-y-auto p-4">
      {messages.map((message, index) => {
        const isLastAssistantMessage =
          message.role === "assistant" &&
          lastExchange?.assistant_message?.id === message.id;

        return (
          <div key={message.id}>
            <ChatMessageItem role={message.role} content={message.content} />

            {isLastAssistantMessage && lastExchange && (
              <ChatGeneratedDeckCard
                savedDeck={lastExchange.saved_deck}
                generationStatus={lastExchange.generation_status}
                invalidCards={lastExchange.invalid_cards}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}