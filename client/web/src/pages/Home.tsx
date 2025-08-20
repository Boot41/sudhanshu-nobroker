import React from "react";
import DisplayCarousel from "../components/DisplayCarousel";
import RegisterPanel from "../components/RegisterPanel";

const Home: React.FC = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        height: "100vh",
        width: "100%",
        overflow: "hidden",
        fontFamily: "var(--font-sans)",
        color: "var(--color-neutral-900)",
        background: "var(--color-neutral-50)",
      }}
    >
      {/* Left: 3/4 marketing carousel (component internally uses width 75% and full height) */}
      <DisplayCarousel />

      {/* Right: 1/4 register panel (component internally uses width 25% and full height) */}
      <RegisterPanel />
    </div>
  );
};

export default Home;
