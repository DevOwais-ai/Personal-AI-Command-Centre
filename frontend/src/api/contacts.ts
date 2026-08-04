import apiClient from "./client";

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

export interface CreateContactData {
  name: string;
  email?: string;
  phone?: string;
  company?: string;
  notes?: string;
}

export interface UpdateContactData {
  name?: string;
  email?: string;
  phone?: string;
  company?: string;
  notes?: string;
}

export async function createContact(
  data: CreateContactData
): Promise<Contact> {
  const response = await apiClient.post<Contact>(
    "/contacts",
    data
  );

  return response.data;
}

export async function getContacts(): Promise<Contact[]> {
  const response = await apiClient.get<Contact[]>(
    "/contacts"
  );

  return response.data;
}

export async function getContact(
  contactId: number
): Promise<Contact> {
  const response = await apiClient.get<Contact>(
    `/contacts/${contactId}`
  );

  return response.data;
}

export async function updateContact(
  contactId: number,
  data: UpdateContactData
): Promise<Contact> {
  const response = await apiClient.patch<Contact>(
    `/contacts/${contactId}`,
    data
  );

  return response.data;
}

export async function deleteContact(
  contactId: number
): Promise<void> {
  await apiClient.delete(`/contacts/${contactId}`);
}
