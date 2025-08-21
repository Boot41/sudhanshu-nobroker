import React, { useState } from "react";
import { AppShell, Stack, Text } from "../ui";
import OwnerSidebar from "../components/owner/OwnerSidebar";
import type { OwnerTab } from "../components/owner/OwnerSidebar";
import PropertiesSummary from "../components/owner/PropertiesSummary";
import PropertiesGrid from "../components/owner/PropertiesGrid";
import PropertiesFilter, { type PropertiesFilterValue } from "../components/owner/PropertiesFilter";
import type { Property } from "../components/owner/PropertyCard";
import { propertyStore } from "../store/propertystore";
import { useEffect } from "react";
import { authStore } from "../store/authstore";

const OwnerDashboard: React.FC = () => {
  const [tab, setTab] = useState<OwnerTab>("properties");
  const [myProps, setMyProps] = useState<Property[]>([]);
  const [publicProps, setPublicProps] = useState<Property[]>([]);
  const [filters, setFilters] = useState<PropertiesFilterValue | null>(null);

  // Auth guard: redirect to /home if not authenticated
  useEffect(() => {
    const { token } = authStore.getState();
    if (!token && typeof window !== "undefined") {
      window.location.assign("/home");
    }
  }, []);

  useEffect(() => {
    const unsubscribe = propertyStore.subscribe((s) => {
      // store uses PropertyOwnerItem which is compatible with PropertyCard's minimal fields
      setMyProps(s.my as unknown as Property[]);
      setPublicProps(s.publicList as unknown as Property[]);
    });
    // initial load
    propertyStore.fetchMy().catch(() => void 0);
    propertyStore.fetchPublic().catch(() => void 0);
    return unsubscribe;
  }, []);

  // In future, we can switch views by tab. For now, dashboard layout is as specified.
  const allProps: Property[] = publicProps;

  const applyFilters = async (v: PropertiesFilterValue) => {
    setFilters(v && (Object.keys(v).length > 0 ? v : null));
    await propertyStore.fetchPublic(v);
  };

  const clearFilters = async () => {
    setFilters(null);
    await propertyStore.fetchPublic();
  };

  // Handle logout tab selection
  useEffect(() => {
    if (tab === "logout") {
      (async () => {
        await authStore.logoutAsync();
        if (typeof window !== "undefined") window.location.assign("/home");
      })();
    }
  }, [tab]);

  return (
    <AppShell sidebar={<OwnerSidebar selected={tab} onSelect={setTab} />}>
      <Stack gap="xl">
        <Stack gap="sm">
          <Text size="2xl" weight={700}>Dashboard</Text>
          <Text color="neutral-600">Manage your properties and applications</Text>
        </Stack>

        {/* Top section: My properties or empty state */}
        <PropertiesSummary properties={myProps} />

        {/* Search Filter between My and All */}
        <PropertiesFilter value={filters || undefined} onApply={applyFilters} onClear={clearFilters} />

        {/* Bottom section: All listed properties */}
        <PropertiesGrid title={filters ? "Filtered Properties" : "All Listed Properties"} properties={allProps} />
      </Stack>
    </AppShell>
  );
};

export default OwnerDashboard;
