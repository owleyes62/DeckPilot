export type ChatMessage = {
  id: number;
  session_id: number;
  role: string;
  content: string;
  created_at: string;
};

export type ChatCard = {
  id: number;
  name: string;
  external_id?: number | null;
  card_type?: string | null;
  race?: string | null;
  attribute?: string | null;
  level?: number | null;
  atk?: number | null;
  defense?: number | null;
  description?: string | null;
  image_url?: string | null;
  image_small_url?: string | null;
  image_cropped_url?: string | null;
  source: string;
};

export type ChatSavedDeckCard = {
  copies: number;
  section: string;
  card: ChatCard;
};

export type ChatSavedDeckDetail = {
  id: number;
  name: string;
  archetype: string;
  play_style: string;
  format: string;
  win_condition?: string | null;
  how_to_pilot?: string | null;
  source: string;
  deck_cards: ChatSavedDeckCard[];
};

export type ChatAIResponse = {
  type: string;
  reply: string;
  intent: string;
  should_ask_questions: boolean;
  questions: string[];
  suggested_archetypes: Array<{
    name: string;
    reason: string;
  }>;
  deck_request?: {
    archetype?: string | null;
    play_style?: string | null;
    format?: string | null;
    goal?: string | null;
    difficulty?: string | null;
    budget?: string | null;
  } | null;
  generated_deck?: unknown;
};

export type ChatMessageExchangeResponse = {
  session_id: number;
  user_message: ChatMessage;
  assistant_message: ChatMessage;
  ai_response: ChatAIResponse;
  saved_deck?: {
    id: number;
    name: string;
    archetype: string;
    play_style: string;
    format: string;
    source: string;
  } | null;
  saved_deck_detail?: ChatSavedDeckDetail | null;
  invalid_cards: string[];
  generation_status: {
    attempted: boolean;
    saved: boolean;
    message: string;
  };
};

export type ChatSessionResponse = {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
};