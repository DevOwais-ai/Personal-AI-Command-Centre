import apiClient from "./client";

export interface Message {
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

export interface InboxStats {
  total: number;
  unread: number;
  important: number;
}

export async function getInboxMessages(): Promise<Message[]> {
  const response = await apiClient.get<Message[]>("/inbox");

  return response.data;
}

export async function getInboxStats(): Promise<InboxStats> {
  const response = await apiClient.get<InboxStats>("/inbox/stats");

  return response.data;
}

export async function markMessageRead(
  messageId: number
): Promise<Message> {
  const response = await apiClient.patch<Message>(
    `/inbox/${messageId}/read`
  );

  return response.data;
}

export async function markMessageUnread(
  messageId: number
): Promise<Message> {
  const response = await apiClient.patch<Message>(
    `/inbox/${messageId}/unread`
  );

  return response.data;
}

export async function markMessageImportant(
  messageId: number
): Promise<Message> {
  const response = await apiClient.patch<Message>(
    `/inbox/${messageId}/important`
  );

  return response.data;
}

export async function markMessageNotImportant(
  messageId: number
): Promise<Message> {
  const response = await apiClient.patch<Message>(
    `/inbox/${messageId}/unimportant`
  );

  return response.data;
}

export async function analyzeMessage(
  messageId: number
): Promise<Message> {
  const response = await apiClient.post<Message>(
    `/inbox/${messageId}/ai/analyze`
  );

  return response.data;
}

export async function retryAIAnalysis(
  messageId: number
): Promise<Message> {
  const response = await apiClient.post<Message>(
    `/inbox/${messageId}/ai/retry`
  );

  return response.data;
}

export async function processPendingAI(): Promise<unknown> {
  const response = await apiClient.post(
    "/inbox/ai/process-pending"
  );

  return response.data;
}
