import apiClient from "./client";

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

export interface CreateAppointmentData {
  title: string;
  description?: string;
  start_at: string;
  end_at: string;
  location?: string;
  contact_id?: number;
}

export interface UpdateAppointmentData {
  title?: string;
  description?: string;
  start_at?: string;
  end_at?: string;
  location?: string;
  contact_id?: number;
  status?: string;
}

export async function createAppointment(
  data: CreateAppointmentData
): Promise<Appointment> {
  const response = await apiClient.post<Appointment>(
    "/appointments",
    data
  );

  return response.data;
}

export async function getAppointments(): Promise<Appointment[]> {
  const response = await apiClient.get<Appointment[]>(
    "/appointments"
  );

  return response.data;
}

export async function getAppointment(
  appointmentId: number
): Promise<Appointment> {
  const response = await apiClient.get<Appointment>(
    `/appointments/${appointmentId}`
  );

  return response.data;
}

export async function updateAppointment(
  appointmentId: number,
  data: UpdateAppointmentData
): Promise<Appointment> {
  const response = await apiClient.patch<Appointment>(
    `/appointments/${appointmentId}`,
    data
  );

  return response.data;
}

export async function deleteAppointment(
  appointmentId: number
): Promise<void> {
  await apiClient.delete(`/appointments/${appointmentId}`);
}