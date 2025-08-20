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

export interface InlineProps extends React.HTMLAttributes<HTMLDivElement> {
  gap?: Space;
  wrap?: boolean;
  align?: React.CSSProperties["alignItems"];
}

export const Inline: React.FC<InlineProps> = ({ gap = "lg", wrap = true, align, style, children, ...rest }) => {
  const base: React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    gap: spaceMap[gap],
    flexWrap: wrap ? "wrap" : "nowrap",
    alignItems: align,
  };
  return (
    <div style={{ ...base, ...style }} {...rest}>
      {children}
    </div>
  );
};

export default Inline;
