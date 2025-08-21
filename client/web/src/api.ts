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

export interface PropertyUpdate {
  name?: string;
  address?: string;
  city?: string;
  state?: string;
  pincode?: string;
  price?: number;
  bedrooms?: number;
  bathrooms?: number;
  area_sqft?: number;
  description?: string | null;
}

export interface PropertyOwnerDetail {
  id: number;
  name: string;
  address: string;
  city: string;
  state: string;
  pincode: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  description?: string | null;
  status: string;
  owner_id: number;
  created_at: string;
  updated_at?: string | null;
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

// Authorized request automatically includes Bearer token if available
async function authorizedRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as any),
  };
  try {
    const token = localStorage.getItem("auth.token");
    if (token) headers["Authorization"] = `Bearer ${token}`;
  } catch {
    // ignore storage issues
  }
  return request<T>(path, { ...options, headers });
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
  logout: () => authorizedRequest<{ message: string }>("/auth/logout", { method: "POST" }),
};

// Property types and API
export interface PropertyCreate {
  name: string;
  address: string;
  city: string;
  state: string;
  pincode: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  description?: string | null;
}

export interface PropertyResponse {
  id: number;
  owner_id: number;
  status: string;
  created_at: string;
  updated_at?: string | null;
  // keep minimal; extend if needed
}

export interface PropertyOwnerItem {
  id: number;
  name: string;
  city: string;
  state: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
}

export interface PropertyPublicItem {
  name: string;
  address: string;
  city: string;
  state: string;
  pincode: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  description?: string | null;
}

export interface PropertyDeleteResponse {
  id: number;
  message: string;
}

export const PropertyAPI = {
  create: (payload: PropertyCreate) =>
    authorizedRequest<PropertyResponse>("/properties/", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listMine: () => authorizedRequest<PropertyOwnerItem[]>("/properties/mine", { method: "GET" }),
  listPublic: (params?: { city?: string; max_price?: number; min_bedrooms?: number; min_area?: number; skip?: number; limit?: number }) => {
    const sp = new URLSearchParams();
    if (params?.city) sp.set("city", params.city);
    if (typeof params?.max_price === "number") sp.set("max_price", String(params.max_price));
    if (typeof params?.min_bedrooms === "number") sp.set("min_bedrooms", String(params.min_bedrooms));
    if (typeof params?.min_area === "number") sp.set("min_area", String(params.min_area));
    if (typeof params?.skip === "number") sp.set("skip", String(params.skip));
    if (typeof params?.limit === "number") sp.set("limit", String(params.limit));
    const q = sp.toString();
    const path = q ? `/properties?${q}` : "/properties";
    return request<PropertyPublicItem[]>(path, { method: "GET" });
  },
  getMine: (id: number) => authorizedRequest<PropertyOwnerDetail>(`/properties/${id}/mine`, { method: "GET" }),
  update: (id: number, updates: PropertyUpdate) =>
    authorizedRequest<PropertyResponse>(`/properties/${id}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    }),
  remove: (id: number) =>
    authorizedRequest<PropertyDeleteResponse>(`/properties/${id}`, {
      method: "DELETE",
    }),
};

export default AuthAPI;
