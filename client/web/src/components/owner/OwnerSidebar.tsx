import React from "react";
import { SidebarContainer, SidebarItem, Text, Divider, Stack } from "../../ui";

export type OwnerTab = "profile" | "properties" | "applications" | "logout";

export type OwnerSidebarProps = {
  selected: OwnerTab;
  onSelect: (tab: OwnerTab) => void;
};

const OwnerSidebar: React.FC<OwnerSidebarProps> = ({ selected, onSelect }) => {
  return (
    <SidebarContainer>
      <Stack gap="md">
        <Text size="xl" weight={700}>Owner Panel</Text>
        <Divider />
        <Stack gap="sm">
          <SidebarItem label="Profile" selected={selected === "profile"} onClick={() => onSelect("profile")} />
          <SidebarItem label="Properties" selected={selected === "properties"} onClick={() => onSelect("properties")} />
          <SidebarItem label="Applications" selected={selected === "applications"} onClick={() => onSelect("applications")} />
        </Stack>
        <Divider />
        <SidebarItem label="Logout" selected={selected === "logout"} onClick={() => onSelect("logout")} />
      </Stack>
    </SidebarContainer>
  );
};

export default OwnerSidebar;
