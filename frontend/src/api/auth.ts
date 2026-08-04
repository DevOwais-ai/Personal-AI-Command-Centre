import apiClient from "./client";

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface UserResponse {
  id: number;
  name: string;
  email: string;
  timezone: string;
  is_active: boolean;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function register(
  data: RegisterData
): Promise<UserResponse> {
  const response = await apiClient.post<UserResponse>(
    "/auth/register",
    data
  );

  return response.data;
}

export async function login(
  data: LoginData
): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>(
    "/auth/login",
    data
  );

  localStorage.setItem(
    "access_token",
    response.data.access_token
  );

  return response.data;
}

export function logout(): void {
  localStorage.removeItem("access_token");
}

export function getAccessToken(): string | null {
  return localStorage.getItem("access_token");
}
