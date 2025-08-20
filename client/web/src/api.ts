// Simple API client using Fetch for auth endpoints
// Base URL is configurable via VITE_API_URL; falls back to localhost:8000

export const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000";

export interface RegisterPayload {
  name: string;
  email: string;
  phone: string;
  password: string;
  user_type: "tenant" | "owner";
}

export interface RegisterResponse {
  id: number | string;
  name: string;
  email: string;
  phone: string;
  user_type: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

async function request<T>(path: string, options: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const message = (isJson && (data?.detail || data?.message)) || res.statusText || "Request failed";
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return data as T;
}

export const AuthAPI = {
  register: (payload: RegisterPayload) =>
    request<RegisterResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  login: (payload: LoginPayload) =>
    request<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export default AuthAPI;
