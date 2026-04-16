type ChatMessageItemProps = {
  role: string;
  content: string;
};

export function ChatMessageItem({ role, content }: ChatMessageItemProps) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-zinc-800 text-zinc-100"
        }`}
      >
        {content}
      </div>
    </div>
  );
}