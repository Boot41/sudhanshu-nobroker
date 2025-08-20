import React from "react";

export interface SwitchProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: React.ReactNode;
}

export const Switch: React.FC<SwitchProps> = ({ label, style, checked, ...rest }) => {
  const track: React.CSSProperties = {
    width: 42,
    height: 24,
    background: checked ? "var(--color-primary-600)" : "var(--color-neutral-300)",
    borderRadius: 999,
    position: "relative",
    transition: "background 150ms ease",
  };
  const thumb: React.CSSProperties = {
    width: 20,
    height: 20,
    background: "var(--color-neutral-50)",
    borderRadius: 999,
    position: "absolute",
    top: 2,
    left: checked ? 20 : 2,
    transition: "left 150ms ease",
  };
  const wrapper: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: "var(--spacing-sm)",
  };

  return (
    <label style={wrapper}>
      <span style={{ ...track, ...style }}>
        <span style={thumb} />
      </span>
      <input type="checkbox" checked={checked} {...rest} style={{ display: "none" }} />
      {label && (
        <span style={{ fontFamily: "var(--font-sans)", color: "var(--color-neutral-800)" }}>{label}</span>
      )}
    </label>
  );
};

export default Switch;
