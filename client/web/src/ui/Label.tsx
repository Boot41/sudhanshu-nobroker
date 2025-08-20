import React from "react";

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  requiredMark?: boolean;
}

export const Label: React.FC<LabelProps> = ({ children, requiredMark, style, ...rest }) => {
  const base: React.CSSProperties = {
    display: "inline-block",
    fontFamily: "var(--font-sans)",
    fontSize: "0.875rem",
    color: "var(--color-neutral-700)",
    marginBottom: "var(--spacing-sm)",
  };

  return (
    <label style={{ ...base, ...style }} {...rest}>
      {children}
      {requiredMark && (
        <span style={{ color: "var(--color-primary-600)", marginLeft: "var(--spacing-xs)" }}>*</span>
      )}
    </label>
  );
};

export default Label;
