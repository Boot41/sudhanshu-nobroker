import React from "react";
import { Panel, Stack, Text, Button, Inline } from "../../ui";
import PropertyCard, { type Property } from "./PropertyCard";

export type PropertiesSummaryProps = {
  properties: Property[];
};

const PropertiesSummary: React.FC<PropertiesSummaryProps> = ({ properties }) => {
  if (!properties || properties.length === 0) {
    return (
      <Panel padding={16} radius={12} shadow>
        <Stack gap="md">
          <Text size="lg" weight={600}>No own property listed yet</Text>
          <Text color="neutral-600">Start by adding your first property.</Text>
          <div>
            <Button
              variant="primary"
              onClick={() => {
                if (typeof window !== "undefined") window.location.assign("/owner/post");
              }}
            >
              Post new property
            </Button>
          </div>
        </Stack>
      </Panel>
    );
  }

  return (
    <Stack gap="md">
      <Inline gap="md" align="center" style={{ justifyContent: "space-between" }}>
        <Text size="xl" weight={700}>My Properties</Text>
        <Button
          variant="primary"
          onClick={() => {
            if (typeof window !== "undefined") window.location.assign("/owner/post");
          }}
        >
          Post new property
        </Button>
      </Inline>
      <Stack gap="md">
        {properties.map((p) => (
          <PropertyCard
            key={p.id}
            property={p}
            footer={
              <Button
                size="sm"
                onClick={() => {
                  if (typeof window !== "undefined") window.location.assign(`/owner/property/${p.id}`);
                }}
              >
                View
              </Button>
            }
          />
        ))}
      </Stack>
    </Stack>
  );
};

export default PropertiesSummary;
