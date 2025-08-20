import React from "react";

export type TextSize = "xs" | "sm" | "md" | "lg" | "xl" | "2xl";
export type TextWeight = 300 | 400 | 500 | 600 | 700;
export type TextColor =
  | "neutral-900"
  | "neutral-700"
  | "neutral-600"
  | "neutral-500"
  | "neutral-400"
  | "primary-600"
  | "secondary-600";

export interface TextProps extends React.HTMLAttributes<HTMLElement> {
  as?: React.ElementType;
  size?: TextSize;
  weight?: TextWeight;
  color?: TextColor;
}

const sizeMap: Record<TextSize, string> = {
  xs: "0.75rem",
  sm: "0.875rem",
  md: "1rem",
  lg: "1.125rem",
  xl: "1.25rem",
  "2xl": "1.5rem",
};

const colorMap: Record<TextColor, string> = {
  "neutral-900": "var(--color-neutral-900)",
  "neutral-700": "var(--color-neutral-700)",
  "neutral-600": "var(--color-neutral-600)",
  "neutral-500": "var(--color-neutral-500)",
  "neutral-400": "var(--color-neutral-400)",
  "primary-600": "var(--color-primary-600)",
  "secondary-600": "var(--color-secondary-600)",
};

export const Text: React.FC<TextProps> = ({
  as = "span",
  size = "md",
  weight = 400,
  color = "neutral-900",
  style,
  children,
  ...rest
}) => {
  const Comp = as as React.ElementType;

  const composedStyle: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    fontSize: sizeMap[size],
    fontWeight: weight,
    color: colorMap[color],
    margin: 0,
    ...style,
  };

  return (
    <Comp style={composedStyle} {...rest}>
      {children}
    </Comp>
  );
};

export default Text;
