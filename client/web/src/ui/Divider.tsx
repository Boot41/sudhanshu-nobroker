import React from "react";

export const Divider: React.FC<React.HTMLAttributes<HTMLHRElement>> = ({ style, ...rest }) => {
  const hrStyle: React.CSSProperties = {
    border: "none",
    borderTop: `1px solid var(--color-neutral-200)`,
    margin: `var(--spacing-lg) 0`,
  };
  return <hr style={{ ...hrStyle, ...style }} {...rest} />;
};

export default Divider;
