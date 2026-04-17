import { api } from "@/lib/api-client";
import type {
  ChatMessage,
  ChatMessageExchangeResponse,
  ChatSessionResponse,
} from "../types/chat.types";

export async function createChatSession(title?: string) {
  const response = await api.post<ChatSessionResponse>("/chat/sessions", {
    title: title ?? null,
  });

  return response.data;
}

export async function sendChatMessage(
  sessionId: number,
  content: string,
) {
  const response = await api.post<ChatMessageExchangeResponse>(
    `/chat/sessions/${sessionId}/messages`,
    { content },
  );

  return response.data;
}

export async function getChatMessages(sessionId: number) {
  const response = await api.get<ChatMessage[]>(
    `/chat/sessions/${sessionId}/messages`,
  );

  return response.data;
}