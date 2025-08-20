import React from "react";

export type Space = "xs" | "sm" | "md" | "lg" | "xl" | "2xl" | "3xl";

const spaceMap: Record<Space, string> = {
  xs: "var(--spacing-xs)",
  sm: "var(--spacing-sm)",
  md: "var(--spacing-md)",
  lg: "var(--spacing-lg)",
  xl: "var(--spacing-xl)",
  "2xl": "var(--spacing-2xl)",
  "3xl": "var(--spacing-3xl)",
};

export interface StackProps extends React.HTMLAttributes<HTMLDivElement> {
  gap?: Space;
  align?: React.CSSProperties["alignItems"];
}

export const Stack: React.FC<StackProps> = ({ gap = "lg", align, style, children, ...rest }) => {
  const base: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: spaceMap[gap],
    alignItems: align,
  };
  return (
    <div style={{ ...base, ...style }} {...rest}>
      {children}
    </div>
  );
};

export default Stack;
