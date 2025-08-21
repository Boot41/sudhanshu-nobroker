import React, { useState, useEffect } from "react";
import { Panel, Stack, Inline, Text, Input, Button } from "../../ui";

export type PropertiesFilterValue = {
  city?: string;
  max_price?: number;
  min_bedrooms?: number;
  min_area?: number;
};

export type PropertiesFilterProps = {
  value?: PropertiesFilterValue;
  onApply: (v: PropertiesFilterValue) => void;
  onClear: () => void;
};

const PropertiesFilter: React.FC<PropertiesFilterProps> = ({ value, onApply, onClear }) => {
  const [city, setCity] = useState<string>(value?.city || "");
  const [maxPrice, setMaxPrice] = useState<string>(value?.max_price != null ? String(value.max_price) : "");
  const [minRooms, setMinRooms] = useState<string>(value?.min_bedrooms != null ? String(value.min_bedrooms) : "");
  const [minArea, setMinArea] = useState<string>(value?.min_area != null ? String(value.min_area) : "");

  useEffect(() => {
    setCity(value?.city || "");
    setMaxPrice(value?.max_price != null ? String(value.max_price) : "");
    setMinRooms(value?.min_bedrooms != null ? String(value.min_bedrooms) : "");
    setMinArea(value?.min_area != null ? String(value.min_area) : "");
  }, [value?.city, value?.max_price, value?.min_bedrooms, value?.min_area]);

  const apply = () => {
    const v: PropertiesFilterValue = {};
    const c = city.trim();
    if (c) v.city = c;
    if (maxPrice.trim() !== "") {
      const n = Number(maxPrice);
      if (!Number.isFinite(n) || n < 0) {
        // simple guard: ignore invalid numbers
        return;
      }
      v.max_price = n;
    }
    if (minRooms.trim() !== "") {
      const r = Number(minRooms);
      if (!Number.isInteger(r) || r < 0) return;
      v.min_bedrooms = r;
    }
    if (minArea.trim() !== "") {
      const a = Number(minArea);
      if (!Number.isFinite(a) || a < 0) return;
      v.min_area = a;
    }
    onApply(v);
  };

  const clear = () => {
    setCity("");
    setMaxPrice("");
    setMinRooms("");
    setMinArea("");
    onClear();
  };

  return (
    <Panel padding={16} radius={12} shadow>
      <Stack gap="md">
        <Text size="xl" weight={700}>Search Properties</Text>
        <Inline gap="md" wrap>
          <Stack gap="xs" style={{ minWidth: 220 }}>
            <Text weight={600}>Location (City)</Text>
            <Input placeholder="e.g. Bengaluru" value={city} onChange={(e) => setCity(e.target.value)} />
          </Stack>
          <Stack gap="xs" style={{ minWidth: 180 }}>
            <Text weight={600}>Max Price</Text>
            <Input type="number" placeholder="e.g. 25000" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
          </Stack>
          <Stack gap="xs" style={{ minWidth: 160 }}>
            <Text weight={600}>Min Rooms</Text>
            <Input type="number" placeholder="e.g. 2" value={minRooms} onChange={(e) => setMinRooms(e.target.value)} />
          </Stack>
          <Stack gap="xs" style={{ minWidth: 180 }}>
            <Text weight={600}>Min Area (sqft)</Text>
            <Input type="number" placeholder="e.g. 800" value={minArea} onChange={(e) => setMinArea(e.target.value)} />
          </Stack>
          <Inline gap="sm" wrap>
            <Button onClick={apply}>Apply Filters</Button>
            <Button variant="outline" onClick={clear}>Clear</Button>
          </Inline>
        </Inline>
      </Stack>
    </Panel>
  );
};

export default PropertiesFilter;
