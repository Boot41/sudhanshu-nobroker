import React, { useEffect, useRef, useState } from "react";
import { AppShell, Stack, Text, Spinner, Button, Inline } from "../ui";
import OwnerSidebar from "../components/owner/OwnerSidebar";
import type { OwnerTab } from "../components/owner/OwnerSidebar";
import PropertyDetails from "../components/owner/PropertyDetails";
import { propertyStore } from "../store/propertystore";
import { authStore } from "../store/authstore";

const PropertyView: React.FC = () => {
  const [tab, setTab] = useState<OwnerTab>("properties");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const [id, setId] = useState<number | null>(null);
  const [detail, setDetail] = useState(propertyStore.getState().current || null);
  const userClicked = useRef(false);

  // Parse id from path and auth guard
  useEffect(() => {
    const { token } = authStore.getState();
    if (!token && typeof window !== "undefined") {
      window.location.assign("/home");
      return;
    }
    if (typeof window !== "undefined") {
      const parts = window.location.pathname.split("/").filter(Boolean);
      const idx = parts.indexOf("property");
      if (idx >= 0 && parts[idx + 1]) {
        const parsed = Number(parts[idx + 1]);
        if (!Number.isFinite(parsed) || parsed <= 0) {
          setError("Invalid property id");
          setLoading(false);
          return;
        }
        setId(parsed);
        setReady(true);
      } else {
        setError("Property id missing in route");
        setLoading(false);
      }
    }
  }, []);

  // Subscribe to store for current property changes
  useEffect(() => {
    const unsub = propertyStore.subscribe((s) => setDetail(s.current || null));
    return unsub;
  }, []);

  // Fetch details
  useEffect(() => {
    if (!ready || id == null) return;
    setLoading(true);
    propertyStore
      .fetchMineById(id)
      .then(() => setLoading(false))
      .catch((e) => {
        setError(e?.message || "Failed to load property");
        setLoading(false);
      });
  }, [ready, id]);

  // Sidebar actions: do not trigger on initial mount
  const didMount = useRef(false);
  useEffect(() => {
    if (!didMount.current) {
      didMount.current = true;
      return;
    }
    if (!userClicked.current) return; // only navigate when user explicitly clicked sidebar
    if (tab === "logout") {
      (async () => {
        await authStore.logoutAsync();
        if (typeof window !== "undefined") window.location.assign("/home");
      })();
    } else if (tab === "properties") {
      if (typeof window !== "undefined") window.location.assign("/owner");
    }
    userClicked.current = false; // reset after handling
  }, [tab]);

  // keep detail from local state synced via subscription

  return (
    <AppShell sidebar={<OwnerSidebar selected={tab} onSelect={(t) => { userClicked.current = true; setTab(t); }} />}>
      <Stack gap="lg">
        <Inline align="center" style={{ justifyContent: "space-between" }}>
          <Stack gap="xs">
            <Text size="2xl" weight={700}>Property Details</Text>
            <Text color="neutral-600">View all information for this property</Text>
          </Stack>
          {!loading && !error && detail && (
            <Inline gap="sm" wrap={false}>
              <Button
                variant="secondary"
                onClick={() => {
                  if (typeof window !== "undefined" && id) {
                    window.location.assign(`/owner/property/${id}/edit`);
                  }
                }}
              >
                Edit
              </Button>
              <Button
                variant="danger"
                onClick={async () => {
                  if (!id) return;
                  const ok = typeof window === "undefined" ? false : window.confirm("Are you sure you want to remove this property?");
                  if (!ok) return;
                  try {
                    await propertyStore.deleteProperty(id);
                    if (typeof window !== "undefined") window.location.assign("/owner");
                  } catch (e: any) {
                    setError(e?.message || "Failed to remove property");
                  }
                }}
              >
                Remove
              </Button>
            </Inline>
          )}
        </Inline>
        {loading && (
          <Stack gap="sm" style={{ alignItems: "center" }}>
            <Spinner />
            <Text>Loading...</Text>
          </Stack>
        )}
        {error && !loading && (
          <Stack gap="sm">
            <Text color="neutral-700">{error}</Text>
            <Button variant="secondary" onClick={() => typeof window !== "undefined" && window.history.back()}>Go Back</Button>
          </Stack>
        )}
        {!loading && !error && detail && (
          <PropertyDetails property={detail} />
        )}
      </Stack>
    </AppShell>
  );
};

export default PropertyView;
