import React from "react";

export type BadgeVariant = "neutral" | "primary" | "secondary";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

const variantStyles: Record<BadgeVariant, React.CSSProperties> = {
  neutral: {
    color: "var(--color-neutral-800)",
    background: "var(--color-neutral-200)",
    border: `1px solid var(--color-neutral-300)`,
  },
  primary: {
    color: "var(--color-neutral-50)",
    background: "var(--color-primary-600)",
    border: `1px solid var(--color-primary-600)`,
  },
  secondary: {
    color: "var(--color-neutral-50)",
    background: "var(--color-secondary-600)",
    border: `1px solid var(--color-secondary-600)`,
  },
};

export const Badge: React.FC<BadgeProps> = ({ variant = "neutral", style, children, ...rest }) => {
  const base: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    fontFamily: "var(--font-sans)",
    fontSize: "0.75rem",
    fontWeight: 600,
    padding: `calc(var(--spacing-xs) + 1px) var(--spacing-sm)`,
    borderRadius: 999,
    gap: "var(--spacing-xs)",
    lineHeight: 1.1,
  };

  return (
    <span style={{ ...base, ...variantStyles[variant], ...style }} {...rest}>
      {children}
    </span>
  );
};

export default Badge;
