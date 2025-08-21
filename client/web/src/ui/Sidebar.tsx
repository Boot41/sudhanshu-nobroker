import React from "react";

export type SidebarContainerProps = {
  children: React.ReactNode;
  width?: number;
  style?: React.CSSProperties;
};

export const SidebarContainer: React.FC<SidebarContainerProps> = ({ children, width = 240, style }) => {
  const base: React.CSSProperties = {
    width,
    height: "100vh",
    position: "sticky",
    top: 0,
    background: "#0f172a", // slate-900
    color: "#e2e8f0", // slate-200
    borderRight: "1px solid #1f2937", // slate-800
    padding: 12,
    display: "flex",
    flexDirection: "column",
    gap: 6,
  };
  return <aside style={{ ...base, ...style }}>{children}</aside>;
};

export type SidebarItemProps = {
  label: string;
  selected?: boolean;
  onClick?: () => void;
  left?: React.ReactNode;
};

export const SidebarItem: React.FC<SidebarItemProps> = ({ label, selected, onClick, left }) => {
  const base: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "10px 12px",
    borderRadius: 8,
    cursor: "pointer",
    color: selected ? "#0f172a" : "#e2e8f0",
    background: selected ? "#e2e8f0" : "transparent",
    userSelect: "none",
  };
  const hover: React.CSSProperties = {
    transition: "background 120ms ease",
  };
  return (
    <div onClick={onClick} style={{ ...base, ...hover }}>
      {left && <span aria-hidden>{left}</span>}
      <span>{label}</span>
    </div>
  );
};
