import React from "react";

export interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: React.ReactNode;
}

export const Radio: React.FC<RadioProps> = ({ label, style, ...rest }) => {
  const wrapper: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: "var(--spacing-sm)",
  };
  const inputStyle: React.CSSProperties = {
    width: 16,
    height: 16,
    accentColor: "var(--color-primary-600)",
  } as React.CSSProperties;

  const labelStyle: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    fontSize: "0.95rem",
    color: "var(--color-neutral-800)",
  };

  return (
    <label style={wrapper}>
      <input type="radio" style={{ ...inputStyle, ...style }} {...rest} />
      {label && <span style={labelStyle}>{label}</span>}
    </label>
  );
};

export default Radio;
