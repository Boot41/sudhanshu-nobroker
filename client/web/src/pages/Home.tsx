import React, { useMemo, useState } from "react";
import DisplayCarousel from "../components/DisplayCarousel";
import RegisterPanel from "../components/RegisterPanel";
import { Stack, Inline, Text, Grid } from "../ui";
import PropertiesFilter, { type PropertiesFilterValue } from "../components/owner/PropertiesFilter";
import PropertyCard from "../components/owner/PropertyCard";
import { PropertyAPI, type PropertyPublicItem } from "../api";

const Home: React.FC = () => {
  const [results, setResults] = useState<PropertyPublicItem[]>([]);
  const [activeFilters, setActiveFilters] = useState<PropertiesFilterValue | undefined>(undefined);
  const hasResults = useMemo(() => (results?.length ?? 0) > 0, [results]);

  const applyFilters = async (v: PropertiesFilterValue) => {
    setActiveFilters(v);
    const list = await PropertyAPI.listPublic(v as any);
    setResults(list);
  };

  const clearFilters = () => {
    setActiveFilters(undefined);
    setResults([]); // Remove shown properties when cleared
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        width: "100%",
        overflowX: "hidden",
        fontFamily: "var(--font-sans)",
        color: "var(--color-neutral-900)",
        background: "var(--color-neutral-50)",
      }}
    >
      {/* Top: Shorter marketing carousel */}
      <div style={{ width: "100%", display: "flex", justifyContent: "center", background: "transparent" }}>
        {/* Edge-to-edge carousel */}
        <DisplayCarousel height={"50vh"} width={"100%"} padding={0} />
      </div>

      {/* Content: Filters and results + Register panel on the right */}
      <div style={{ width: "100%", boxSizing: "border-box", padding: 0 }}>
        <Inline gap="xl" wrap style={{ alignItems: "flex-start", justifyContent: "space-between" }}>
          {/* Left: Filters and (conditional) results */}
          <div style={{ flex: 1, minWidth: 360, maxWidth: "100%" }}>
            <Stack gap="xl">
              <PropertiesFilter value={activeFilters} onApply={applyFilters} onClear={clearFilters} />

              {hasResults ? (
                <Stack gap="md">
                  <Text as="h3" size="xl" weight={700}>Search Results</Text>
                  <Grid minColWidth={280} gap={16}>
                    {results.map((p, idx) => (
                      <PropertyCard key={idx} property={p as any} />
                    ))}
                  </Grid>
                </Stack>
              ) : (
                <Text color="neutral-600">Apply filters to see properties here.</Text>
              )}
            </Stack>
          </div>

          {/* Right: Register panel */}
          <div style={{ width: 360, flexShrink: 0 }}>
            <RegisterPanel />
          </div>
        </Inline>
      </div>
    </div>
  );
};

export default Home;
