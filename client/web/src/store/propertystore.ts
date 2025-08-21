import { PropertyAPI, type PropertyCreate, type PropertyResponse, type PropertyOwnerItem, type PropertyOwnerDetail, type PropertyPublicItem } from "../api";

export interface PropertyState {
  creating: boolean;
  error: string | null;
  lastCreated?: PropertyResponse | null;
  my: PropertyOwnerItem[];
  loadingMy: boolean;
  errorMy: string | null;
  current?: PropertyOwnerDetail | null;
  loadingCurrent: boolean;
  errorCurrent: string | null;
  publicList: PropertyPublicItem[];
  loadingPublic: boolean;
  errorPublic: string | null;
}

export type PropertyListener = (state: PropertyState) => void;

class PropertyStore {
  private state: PropertyState = { creating: false, error: null, lastCreated: null, my: [], loadingMy: false, errorMy: null, current: null, loadingCurrent: false, errorCurrent: null, publicList: [], loadingPublic: false, errorPublic: null };
  private listeners: Set<PropertyListener> = new Set();

  getState(): PropertyState {
    return this.state;
  }

  subscribe(listener: PropertyListener): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  private set(partial: Partial<PropertyState>) {
    this.state = { ...this.state, ...partial };
    this.listeners.forEach((l) => l(this.state));
  }

  async createProperty(payload: PropertyCreate): Promise<PropertyResponse> {
    try {
      this.set({ creating: true, error: null });
      const res = await PropertyAPI.create(payload);
      this.set({ creating: false, lastCreated: res });
      // After creating, refresh my properties list in the background (best effort)
      this.fetchMy().catch(() => void 0);
      return res;
    } catch (e: any) {
      const msg = e?.message || "Failed to create property";
      this.set({ creating: false, error: msg });
      throw new Error(msg);
    }
  }

  async fetchMy(): Promise<PropertyOwnerItem[]> {
    try {
      this.set({ loadingMy: true, errorMy: null });
      const list = await PropertyAPI.listMine();
      this.set({ loadingMy: false, my: list });
      return list;
    } catch (e: any) {
      const msg = e?.message || "Failed to load your properties";
      this.set({ loadingMy: false, errorMy: msg });
      throw new Error(msg);
    }
  }

  async fetchMineById(id: number): Promise<PropertyOwnerDetail> {
    try {
      this.set({ loadingCurrent: true, errorCurrent: null });
      const detail = await PropertyAPI.getMine(id);
      this.set({ loadingCurrent: false, current: detail });
      return detail;
    } catch (e: any) {
      const msg = e?.message || "Failed to load property details";
      this.set({ loadingCurrent: false, errorCurrent: msg });
      throw new Error(msg);
    }
  }

  async fetchPublic(params?: { city?: string; max_price?: number; min_bedrooms?: number; min_area?: number; skip?: number; limit?: number }): Promise<PropertyPublicItem[]> {
    try {
      this.set({ loadingPublic: true, errorPublic: null });
      const list = await PropertyAPI.listPublic(params);
      this.set({ loadingPublic: false, publicList: list });
      return list;
    } catch (e: any) {
      const msg = e?.message || "Failed to load properties";
      this.set({ loadingPublic: false, errorPublic: msg });
      throw new Error(msg);
    }
  }

  async updateProperty(id: number, updates: Partial<PropertyOwnerDetail>): Promise<void> {
    // Only send fields allowed by API update type
    const payload: any = {
      name: updates.name,
      address: updates.address,
      city: updates.city,
      state: updates.state,
      pincode: updates.pincode,
      price: updates.price,
      bedrooms: updates.bedrooms,
      bathrooms: updates.bathrooms,
      area_sqft: updates.area_sqft,
      description: updates.description,
    };
    await PropertyAPI.update(id, payload);
    // Refresh current and lists
    try { await this.fetchMineById(id); } catch {}
    try { await this.fetchMy(); } catch {}
    try { await this.fetchPublic(); } catch {}
  }

  async deleteProperty(id: number): Promise<void> {
    await PropertyAPI.remove(id);
    // Remove from local lists
    const nextMy = (this.state.my || []).filter((p) => p.id !== id);
    const nextPublic = (this.state.publicList || []).filter((p: any) => p.id !== id);
    const next: Partial<PropertyState> = { my: nextMy, publicList: nextPublic };
    if (this.state.current && this.state.current.id === id) next.current = null;
    this.set(next as PropertyState);
  }
}

export const propertyStore = new PropertyStore();
export default propertyStore;
