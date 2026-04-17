import { ChatMessageItem } from "./chat-message-item";
import type { ChatMessage } from "@/features/chat/types/chat.types";

type ChatMessageListProps = {
  messages: ChatMessage[];
};

export function ChatMessageList({ messages }: ChatMessageListProps) {
  return (
    <div className="flex h-full flex-col gap-3 overflow-y-auto p-4">
      {messages.map((message) => (
        <ChatMessageItem
          key={message.id}
          role={message.role}
          content={message.content}
        />
      ))}
    </div>
  );
}