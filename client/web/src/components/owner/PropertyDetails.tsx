import React from "react";
import { Panel, Stack, Text, Divider, Inline } from "../../ui";
import type { PropertyOwnerDetail } from "../../api";

export type PropertyDetailsProps = {
  property: PropertyOwnerDetail;
};

const Row: React.FC<{ label: string; value: React.ReactNode }> = ({ label, value }) => (
  <Inline gap="sm" align="baseline">
    <Text weight={600}>{label}:</Text>
    <Text>{value as any}</Text>
  </Inline>
);

const PropertyDetails: React.FC<PropertyDetailsProps> = ({ property }) => {
  return (
    <Panel padding={20} radius={12} shadow>
      <Stack gap="md">
        <Stack gap="xs">
          <Text size="2xl" weight={700}>{property.name}</Text>
          <Text color="neutral-600">ID #{property.id}</Text>
        </Stack>
        <Divider />
        <Stack gap="sm">
          <Row label="Address" value={property.address} />
          <Row label="City" value={`${property.city}, ${property.state} ${property.pincode}`} />
          <Row label="Price" value={`₹ ${property.price.toLocaleString()}`} />
          <Row label="Bedrooms" value={property.bedrooms} />
          <Row label="Bathrooms" value={property.bathrooms} />
          <Row label="Area" value={`${property.area_sqft} sqft`} />
          {property.description ? <Row label="Description" value={property.description} /> : null}
          <Row label="Status" value={property.status} />
          <Row label="Owner ID" value={property.owner_id} />
          <Row label="Created At" value={new Date(property.created_at).toLocaleString()} />
          {property.updated_at ? <Row label="Updated At" value={new Date(property.updated_at).toLocaleString()} /> : null}
        </Stack>
      </Stack>
    </Panel>
  );
};

export default PropertyDetails;
