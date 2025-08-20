import React from "react";

export interface SelectOption {
  label: string;
  value: string | number;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  helperText?: string;
  error?: string;
  fullWidth?: boolean;
  options?: SelectOption[];
}

export const Select: React.FC<SelectProps> = ({
  label,
  helperText,
  error,
  fullWidth,
  style,
  id,
  options,
  children,
  ...rest
}) => {
  const selectId = id || rest.name || `select-${Math.random().toString(36).slice(2, 7)}`;

  const labelStyle: React.CSSProperties = {
    display: "block",
    fontFamily: "var(--font-sans)",
    fontSize: "0.875rem",
    color: "var(--color-neutral-700)",
    marginBottom: "var(--spacing-sm)",
  };

  const selectStyle: React.CSSProperties = {
    width: fullWidth ? "100%" : undefined,
    fontFamily: "var(--font-sans)",
    fontSize: "1rem",
    color: "var(--color-neutral-900)",
    background: "var(--color-neutral-50)",
    border: `1px solid ${error ? "var(--color-primary-600)" : "var(--color-neutral-300)"}`,
    borderRadius: 6,
    padding: `var(--spacing-md) var(--spacing-lg)`,
    outline: "none",
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
        <label htmlFor={selectId} style={labelStyle}>
          {label}
        </label>
      )}
      <select id={selectId} style={{ ...selectStyle, ...style }} {...rest}>
        {options
          ? options.map((opt) => (
              <option key={String(opt.value)} value={opt.value}>
                {opt.label}
              </option>
            ))
          : children}
      </select>
      {(helperText || error) && <div style={helperStyle}>{error ? error : helperText}</div>}
    </div>
  );
};

export default Select;
