import React from "react";

export interface LinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {}

export const Link: React.FC<LinkProps> = ({ style, children, ...rest }) => {
  const base: React.CSSProperties = {
    color: "var(--color-primary-600)",
    textDecoration: "none",
    fontFamily: "var(--font-sans)",
  };
  // Inline hover isn't possible purely via style object; rely on default hover underline via browser focus/active states.
  return (
    <a style={{ ...base, ...style }} {...rest}>
      {children}
    </a>
  );
};

export default Link;
