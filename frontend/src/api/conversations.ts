import apiClient from "./client";

export interface Conversation {
  id: number;
  user_id: number;
  integration_id?: number | null;
  contact_id?: number | null;
  platform: string;
  external_id?: string | null;
  title?: string | null;
  status: string;
  last_message_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ConversationMessage {
  id: number;
  user_id: number;
  conversation_id: number;
  platform: string;
  external_id?: string | null;
  direction: string;
  sender_name?: string | null;
  sender_identifier?: string | null;
  recipient_identifier?: string | null;
  content: string;
  message_type: string;
  is_read: boolean;
  is_important: boolean;
  ai_summary?: string | null;
  ai_category?: string | null;
  ai_priority?: string | null;
  ai_intent?: string | null;
  ai_action_required: boolean;
  ai_processed: boolean;
  ai_status: string;
  received_at: string;
  created_at: string;
}

export interface CreateConversationData {
  platform: string;
  external_id?: string;
  title?: string;
  integration_id?: number;
  contact_id?: number;
}

export async function createConversation(
  data: CreateConversationData
): Promise<Conversation> {
  const response = await apiClient.post<Conversation>(
    "/conversations",
    data
  );

  return response.data;
}

export async function getConversations(): Promise<Conversation[]> {
  const response = await apiClient.get<Conversation[]>(
    "/conversations"
  );

  return response.data;
}

export async function getConversation(
  conversationId: number
): Promise<Conversation> {
  const response = await apiClient.get<Conversation>(
    `/conversations/${conversationId}`
  );

  return response.data;
}

export async function getConversationMessages(
  conversationId: number
): Promise<ConversationMessage[]> {
  const response = await apiClient.get<ConversationMessage[]>(
    `/conversations/${conversationId}/messages`
  );

  return response.data;
}

export async function analyzeConversationMessage(
  conversationId: number,
  messageId: number
): Promise<ConversationMessage> {
  const response = await apiClient.post<ConversationMessage>(
    `/conversations/${conversationId}/messages/${messageId}/ai/analyze`
  );

  return response.data;
}
