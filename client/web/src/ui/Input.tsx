import React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  fullWidth?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  helperText,
  error,
  fullWidth,
  style,
  id,
  ...rest
}) => {
  const inputId = id || rest.name || `input-${Math.random().toString(36).slice(2, 7)}`;

  const labelStyle: React.CSSProperties = {
    display: "block",
    fontFamily: "var(--font-sans)",
    fontSize: "0.875rem",
    color: "var(--color-neutral-700)",
    marginBottom: "var(--spacing-sm)",
  };

  const inputStyle: React.CSSProperties = {
    width: fullWidth ? "100%" : undefined,
    fontFamily: "var(--font-sans)",
    fontSize: "1rem",
    color: "var(--color-neutral-900)",
    background: "var(--color-neutral-50)",
    border: `1px solid ${error ? "var(--color-primary-600)" : "var(--color-neutral-300)"}`,
    borderRadius: 6,
    padding: `var(--spacing-md) var(--spacing-lg)`,
    outline: "none",
    boxShadow: "none",
  };

  const helperStyle: React.CSSProperties = {
    fontFamily: "var(--font-sans)",
    fontSize: "0.75rem",
    color: error ? "var(--color-primary-600)" : "var(--color-neutral-600)",
    marginTop: "var(--spacing-sm)",
  };

  return (
    <div style={{ width: fullWidth ? "100%" : undefined }}>
      {label && (
        <label htmlFor={inputId} style={labelStyle}>
          {label}
        </label>
      )}
      <input id={inputId} style={{ ...inputStyle, ...style }} {...rest} />
      {(helperText || error) && (
        <div style={helperStyle}>{error ? error : helperText}</div>
      )}
    </div>
  );
};

export default Input;
