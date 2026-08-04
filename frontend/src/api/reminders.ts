import apiClient from "./client";

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

export interface CreateReminderData {
  title: string;
  remind_at: string;
  notification_channel?: string;
  task_id?: number;
  appointment_id?: number;
}

export async function createReminder(
  data: CreateReminderData
): Promise<Reminder> {
  const response = await apiClient.post<Reminder>(
    "/reminders",
    data
  );

  return response.data;
}

export async function getReminders(): Promise<Reminder[]> {
  const response = await apiClient.get<Reminder[]>(
    "/reminders"
  );

  return response.data;
}
