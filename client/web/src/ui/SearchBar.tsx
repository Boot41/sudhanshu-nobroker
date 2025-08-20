import React, { useState } from "react";
import { Button } from "./Button";

export interface SearchBarProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (value: string) => void;
  fullWidth?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = "Search...",
  value,
  onChange,
  onSearch,
  fullWidth,
}) => {
  const [internal, setInternal] = useState("");
  const val = value !== undefined ? value : internal;

  const containerStyle: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: "var(--spacing-sm)",
    width: fullWidth ? "100%" : undefined,
  };

  const inputStyle: React.CSSProperties = {
    flex: 1,
    fontFamily: "var(--font-sans)",
    fontSize: "1rem",
    color: "var(--color-neutral-900)",
    background: "var(--color-neutral-50)",
    border: `1px solid var(--color-neutral-300)`,
    borderRadius: 6,
    padding: `var(--spacing-md) var(--spacing-lg)`,
    outline: "none",
  };

  const handleSearch = () => {
    if (onSearch) onSearch(val);
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <div style={containerStyle}>
      <span
        aria-hidden
        style={{
          color: "var(--color-neutral-500)",
          marginRight: "var(--spacing-sm)",
        }}
      >
        🔍
      </span>
      <input
        type="search"
        placeholder={placeholder}
        value={val}
        onChange={(e) => {
          onChange?.(e.target.value);
          if (value === undefined) setInternal(e.target.value);
        }}
        onKeyDown={handleKeyDown}
        style={inputStyle}
      />
      <Button variant="secondary" onClick={handleSearch}>
        Search
      </Button>
    </div>
  );
};

export default SearchBar;
