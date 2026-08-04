import apiClient from "./client";

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  priority: string;
  due_at?: string | null;
  status: string;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  priority?: string;
  due_at?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  priority?: string;
  due_at?: string;
  status?: string;
}

export async function createTask(
  data: CreateTaskData
): Promise<Task> {
  const response = await apiClient.post<Task>(
    "/tasks",
    data
  );

  return response.data;
}

export async function getTasks(): Promise<Task[]> {
  const response = await apiClient.get<Task[]>("/tasks");

  return response.data;
}

export async function getTask(
  taskId: number
): Promise<Task> {
  const response = await apiClient.get<Task>(
    `/tasks/${taskId}`
  );

  return response.data;
}

export async function updateTask(
  taskId: number,
  data: UpdateTaskData
): Promise<Task> {
  const response = await apiClient.patch<Task>(
    `/tasks/${taskId}`,
    data
  );

  return response.data;
}

export async function deleteTask(
  taskId: number
): Promise<void> {
  await apiClient.delete(`/tasks/${taskId}`);
}
