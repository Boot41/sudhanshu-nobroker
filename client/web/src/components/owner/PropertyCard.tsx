import React from "react";
import { Panel, Text, Stack } from "../../ui";

export type Property = {
  id?: number;
  name: string;
  city: string;
  state: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
};

export type PropertyCardProps = {
  property: Property;
  footer?: React.ReactNode;
};

const PropertyCard: React.FC<PropertyCardProps> = ({ property, footer }) => {
  const { name, city, state, price, bedrooms, bathrooms, area_sqft } = property;
  return (
    <Panel padding={16} radius={12} shadow>
      <Stack gap="sm">
        <Stack gap="xs">
          <Text size="lg" weight={600}>{name}</Text>
          <Text color="neutral-600">{city}, {state}</Text>
        </Stack>
        <Stack gap="xs">
          <Text><strong>Price:</strong> ₹ {price.toLocaleString()}</Text>
          <Text><strong>Beds:</strong> {bedrooms}  <strong>Baths:</strong> {bathrooms}  <strong>Area:</strong> {area_sqft} sqft</Text>
        </Stack>
        {footer ? footer : null}
      </Stack>
    </Panel>
  );
};

export default PropertyCard;
