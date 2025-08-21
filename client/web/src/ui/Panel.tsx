import React from "react";

export type PanelProps = {
  children: React.ReactNode;
  padding?: number;
  radius?: number;
  shadow?: boolean;
  fullWidth?: boolean;
  style?: React.CSSProperties;
};

export const Panel: React.FC<PanelProps> = ({
  children,
  padding = 16,
  radius = 12,
  shadow = true,
  fullWidth = false,
  style,
}) => {
  const base: React.CSSProperties = {
    background: "#fff",
    border: "1px solid var(--neutral-200)",
    borderRadius: radius,
    padding,
    width: fullWidth ? "100%" : undefined,
    boxShadow: shadow ? "0 1px 2px rgba(0,0,0,0.06)" : undefined,
  };
  return <div style={{ ...base, ...style }}>{children}</div>;
};
