import React from "react";

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: React.ReactNode;
  error?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({ label, error, style, ...rest }) => {
  const wrapper: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: "var(--spacing-sm)",
  };
  const boxStyle: React.CSSProperties = {
    width: 16,
    height: 16,
    accentColor: "var(--color-primary-600)",
  } as React.CSSProperties;

  const labelStyle: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    fontSize: "0.95rem",
    color: "var(--color-neutral-800)",
  };

  const errorStyle: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    fontSize: "0.75rem",
    color: "var(--color-primary-600)",
    marginTop: "var(--spacing-xs)",
  };

  return (
    <div>
      <label style={wrapper}>
        <input type="checkbox" style={{ ...boxStyle, ...style }} {...rest} />
        {label && <span style={labelStyle}>{label}</span>}
      </label>
      {error && <div style={errorStyle}>{error}</div>}
    </div>
  );
};

export default Checkbox;
