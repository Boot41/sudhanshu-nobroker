import { AuthAPI, type LoginPayload, type RegisterPayload, type TokenResponse } from "../api";

// Minimal global store implementation (no external deps)
// Usage:
// import { authStore } from "../store/authstore";
// authStore.subscribe((s) => console.log("auth state:", s));
// await authStore.login({ email, password })

export interface AuthUser {
  id?: string | number;
  name?: string;
  email?: string;
  phone?: string;
  user_type?: string;
}

export interface AuthState {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export type AuthListener = (state: AuthState) => void;

function loadPersisted(): Pick<AuthState, "user" | "token"> {
  try {
    const token = localStorage.getItem("auth.token");
    const userRaw = localStorage.getItem("auth.user");
    const user = userRaw ? (JSON.parse(userRaw) as AuthUser) : null;
    return { token, user };
  } catch {
    return { token: null, user: null };
  }
}

function persist(state: Pick<AuthState, "user" | "token">) {
  try {
    if (state.token) localStorage.setItem("auth.token", state.token);
    else localStorage.removeItem("auth.token");
    if (state.user) localStorage.setItem("auth.user", JSON.stringify(state.user));
    else localStorage.removeItem("auth.user");
  } catch {
    // noop
  }
}

class AuthStore {
  private state: AuthState;
  private listeners: Set<AuthListener> = new Set();

  constructor() {
    const persisted = typeof window !== "undefined" ? loadPersisted() : { token: null, user: null };
    this.state = {
      user: persisted.user,
      token: persisted.token,
      loading: false,
      error: null,
    };
  }

  getState(): AuthState {
    return this.state;
  }

  subscribe(listener: AuthListener): () => void {
    this.listeners.add(listener);
    // emit current state immediately
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  private set(partial: Partial<AuthState>) {
    this.state = { ...this.state, ...partial };
    // persist token/user when they change
    persist({ token: this.state.token, user: this.state.user });
    this.listeners.forEach((l) => l(this.state));
  }

  async register(payload: RegisterPayload) {
    try {
      this.set({ loading: true, error: null });
      const res = await AuthAPI.register(payload);
      // Keep user minimal until login; API may return created user fields
      const user: AuthUser = {
        id: (res as any).id,
        name: (res as any).name,
        email: (res as any).email,
        phone: (res as any).phone,
        user_type: (res as any).user_type,
      };
      // Do not auto-login unless backend returns token; keep token null
      this.set({ user, loading: false, error: null });
      return res;
    } catch (e: any) {
      this.set({ loading: false, error: e?.message || "Registration failed" });
      throw e;
    }
  }

  async login(payload: LoginPayload) {
    try {
      this.set({ loading: true, error: null });
      const tokenRes: TokenResponse = await AuthAPI.login(payload);
      // If you have a me/profile endpoint, fetch user details here
      this.set({ token: tokenRes.access_token, loading: false, error: null });
      return tokenRes;
    } catch (e: any) {
      this.set({ loading: false, error: e?.message || "Login failed" });
      throw e;
    }
  }

  logout() {
    this.set({ token: null, user: null, error: null });
  }

  async logoutAsync() {
    try {
      // Best-effort server-side logout (for future revocation/audit). Ignore errors.
      await AuthAPI.logout();
    } catch {
      // noop
    } finally {
      this.logout();
    }
  }
}

export const authStore = new AuthStore();
export default authStore;
