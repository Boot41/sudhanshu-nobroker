import React from "react";

export type ButtonVariant = "primary" | "secondary" | "outline" | "ghost" | "danger";
export type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
}

const sizeStyles: Record<ButtonSize, React.CSSProperties> = {
  sm: {
    padding: `var(--spacing-sm) var(--spacing-lg)`,
  },
  md: {
    padding: `var(--spacing-md) var(--spacing-xl)`,
  },
  lg: {
    padding: `var(--spacing-lg) var(--spacing-2xl)`,
  },
};

const getVariantStyles = (variant: ButtonVariant, disabled?: boolean): React.CSSProperties => {
  const base: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    color: "var(--color-neutral-50)",
    background: "var(--color-primary-600)",
    border: `1px solid var(--color-primary-600)`,
    opacity: disabled ? 0.6 : 1,
    cursor: disabled ? "not-allowed" : "pointer",
  };

  switch (variant) {
    case "secondary":
      return {
        ...base,
        background: "var(--color-secondary-600)",
        border: `1px solid var(--color-secondary-600)`,
      };
    case "outline":
      return {
        ...base,
        background: "var(--color-neutral-50)",
        color: "var(--color-neutral-900)",
        border: `1px solid var(--color-neutral-300)`,
      };
    case "ghost":
      return {
        ...base,
        background: "var(--color-neutral-50)",
        color: "var(--color-primary-600)",
        border: `1px solid var(--color-neutral-50)`,
      };
    case "danger":
      return {
        ...base,
        background: "var(--color-primary-700)",
        border: `1px solid var(--color-primary-700)`,
      };
    case "primary":
    default:
      return base;
  }
};

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  fullWidth,
  style,
  ...rest
}) => {
  const composedStyle: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "var(--spacing-sm)",
    lineHeight: 1.2,
    userSelect: "none",
    textDecoration: "none",
    fontWeight: 600,
    borderRadius: 8,
    boxShadow: "0 1px 2px rgba(0,0,0,0.08)",
    transition: "transform 120ms ease, box-shadow 120ms ease, opacity 120ms ease",
    width: fullWidth ? "100%" : undefined,
    ...sizeStyles[size],
    ...getVariantStyles(variant, rest.disabled),
    ...style,
  };

  return (
    <button style={composedStyle} {...rest}>
      {children}
    </button>
  );
};

export default Button;
