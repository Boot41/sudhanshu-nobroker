import React from "react";
import { Grid, Text, Stack } from "../../ui";
import PropertyCard, { type Property } from "./PropertyCard";

export type PropertiesGridProps = {
  title: string;
  properties: Property[];
};

const PropertiesGrid: React.FC<PropertiesGridProps> = ({ title, properties }) => {
  return (
    <Stack gap="md">
      <Text size="xl" weight={600}>{title}</Text>
      <Grid minColWidth={280} gap={16}>
        {properties.map((p, idx) => (
          <PropertyCard key={p.id ?? `${p.name}-${p.city}-${p.price}-${idx}`} property={p} />
        ))}
      </Grid>
    </Stack>
  );
};

export default PropertiesGrid;
