import React from "react";

export type GridProps = {
  columns?: number;
  minColWidth?: number; // when provided, uses auto-fit minmax
  gap?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
};

export const Grid: React.FC<GridProps> = ({ columns = 3, minColWidth, gap = 16, children, style }) => {
  const gridTemplateColumns = minColWidth
    ? `repeat(auto-fit, minmax(${minColWidth}px, 1fr))`
    : `repeat(${columns}, 1fr)`;
  const base: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns,
    gap,
  };
  return <div style={{ ...base, ...style }}>{children}</div>;
};
