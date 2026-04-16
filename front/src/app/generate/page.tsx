import { ChatContainer } from "@/components/chat/chat-container";
import { DeckViewer } from "@/components/deck/deck-viewer";

export default function GeneratePage() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 p-6 lg:flex-row">
        <section className="w-full lg:w-[45%]">
          <ChatContainer />
        </section>

        <section className="w-full lg:w-[55%]">
          <DeckViewer />
        </section>
      </div>
    </main>
  );
}