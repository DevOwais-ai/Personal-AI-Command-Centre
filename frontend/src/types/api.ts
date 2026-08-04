export interface User {
  id: number;
  name: string;
  email: string;
  timezone: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: number;
  user_id: number;
  name: string;
  email?: string | null;
  phone?: string | null;
  company?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
}

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

export interface Reminder {
  id: number;
  user_id: number;
  task_id?: number | null;
  appointment_id?: number | null;
  title: string;
  remind_at: string;
  notification_channel: string;
  status: string;
  sent_at?: string | null;
  created_at: string;
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  priority: string;
  status: string;
  due_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: number;
  user_id: number;
  contact_id?: number | null;
  title: string;
  description?: string | null;
  start_at: string;
  end_at: string;
  location?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface AIAction {
  id: number;
  user_id: number;
  message_id: number;
  action_type: string;
  agent: string;
  input_data?: Record<string, unknown> | null;
  output_data?: Record<string, unknown> | null;
  status: string;
  requires_approval: boolean;
  approved?: boolean | null;
  created_at: string;
}

export interface APIError {
  detail: string;
}
