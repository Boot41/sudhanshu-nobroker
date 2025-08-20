import React, { useEffect, useMemo, useState } from "react";
import { Stack, Text, Badge } from "../ui";

export interface DisplayCarouselSlide {
  title: string;
  subtitle: string;
  accent?: string; // token name like 'primary' | 'secondary'
  background?: string; // css color or token
}

export interface DisplayCarouselProps {
  slides?: DisplayCarouselSlide[];
  autoAdvanceMs?: number;
  height?: number | string;
  onSlideChange?: (index: number) => void;
}

/**
 * A 3/4 width, full-height marketing carousel with auto-rotation.
 * Uses only atoms from ../ui: Stack, Inline, Text, Button, Badge
 */
const DisplayCarousel: React.FC<DisplayCarouselProps> = ({
  slides,
  autoAdvanceMs = 5000,
  height = "100vh",
  onSlideChange,
}) => {
  const data = useMemo<DisplayCarouselSlide[]>(
    () =>
      slides ?? [
        {
          title: "Find homes without paying brokerage",
          subtitle: "Browse verified listings and connect directly with owners. Save money, time, and hassle.",
          accent: "primary",
          background: "linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100))",
        },
        {
          title: "List your property in minutes",
          subtitle: "Reach thousands of genuine tenants. Manage enquiries and applications with ease.",
          accent: "secondary",
          background: "linear-gradient(135deg, var(--color-secondary-50), var(--color-secondary-100))",
        },
        {
          title: "Smart filters. Real results.",
          subtitle: "Pin-point the right home by location, budget, amenities, and more — all in one place.",
          accent: "primary",
          background: "linear-gradient(135deg, var(--color-neutral-50), var(--color-neutral-100))",
        },
      ],
    [slides]
  );

  const [index, setIndex] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => {
      setIndex((i) => (i + 1) % data.length);
    }, autoAdvanceMs);
    return () => window.clearInterval(id);
  }, [autoAdvanceMs, data.length]);

  useEffect(() => {
    onSlideChange?.(index);
  }, [index, onSlideChange]);

  // Auto-advances via interval above; manual controls removed per design

  const current = data[index];

  return (
    <section
      style={{
        width: "75%",
        height,
        boxSizing: "border-box",
        padding: "var(--spacing-3xl)",
        background: current.background ?? "var(--color-neutral-50)",
        color: "var(--color-neutral-900)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ width: "min(900px, 100%)" }}>
        <Stack gap="2xl">
          <Badge variant={current.accent === "secondary" ? "secondary" : "primary"}>
            {current.accent === "secondary" ? "For Owners" : "For Everyone"}
          </Badge>

          <Text as="h2" size="2xl" weight={700}>
            {current.title}
          </Text>

          <Text as="p" size="lg" color="neutral-700">
            {current.subtitle}
          </Text>

        </Stack>
      </div>
    </section>
  );
};

export default DisplayCarousel;
