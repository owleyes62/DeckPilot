import { ChatInput } from "./chat-input";
import { ChatMessageList } from "./chat-message-list";

const mockMessages = [
  {
    id: 1,
    role: "assistant",
    content: "Olá! Me diga que tipo de deck você quer montar e eu te ajudo.",
  },
];

export function ChatContainer() {
  return (
    <div className="flex h-[80vh] flex-col rounded-2xl border border-zinc-800 bg-zinc-900">
      <div className="border-b border-zinc-800 p-4">
        <h1 className="text-lg font-semibold">DeckPilot Chat</h1>
        <p className="text-sm text-zinc-400">
          Converse com a IA para gerar ou refinar um deck.
        </p>
      </div>

      <div className="flex-1 overflow-hidden">
        <ChatMessageList messages={mockMessages} />
      </div>

      <div className="border-t border-zinc-800 p-4">
        <ChatInput />
      </div>
    </div>
  );
}