import React from "react";

export interface SpinnerProps extends React.SVGProps<SVGSVGElement> {
  size?: number;
  color?: "primary" | "secondary" | "neutral";
}

const colorMap = {
  primary: "var(--color-primary-600)",
  secondary: "var(--color-secondary-600)",
  neutral: "var(--color-neutral-600)",
} as const;

export const Spinner: React.FC<SpinnerProps> = ({ size = 20, color = "primary", ...rest }) => {
  const stroke = colorMap[color];
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 50 50"
      fill="none"
      {...rest}
      role="img"
      aria-label="loading"
    >
      <circle cx="25" cy="25" r="20" stroke="var(--color-neutral-200)" strokeWidth="6" />
      <path
        d="M45 25c0-11.046-8.954-20-20-20"
        stroke={stroke}
        strokeWidth="6"
      >
        <animateTransform
          attributeName="transform"
          type="rotate"
          from="0 25 25"
          to="360 25 25"
          dur="0.8s"
          repeatCount="indefinite"
        />
      </path>
    </svg>
  );
};

export default Spinner;
