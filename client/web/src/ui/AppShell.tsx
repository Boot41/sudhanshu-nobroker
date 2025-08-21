import React from "react";

export type AppShellProps = {
  sidebar: React.ReactNode;
  children: React.ReactNode;
};

export const AppShell: React.FC<AppShellProps> = ({ sidebar, children }) => {
  const base: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "260px 1fr",
    minHeight: "100vh",
    background: "#f8fafc", // slate-50
  };
  return (
    <div style={base}>
      {sidebar}
      <main style={{ padding: 0, width: "100%" }}>{children}</main>
    </div>
  );
};
