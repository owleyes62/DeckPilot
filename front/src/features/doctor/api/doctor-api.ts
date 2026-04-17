import { api } from "@/lib/api-client";
import type { DoctorDeck } from "../types/doctor.types";

export async function getDoctorAnalysis(deckId: number) {
  const response = await api.get<DoctorDeck>(`/doctor/decks/${deckId}/ai`);
  return response.data;
}