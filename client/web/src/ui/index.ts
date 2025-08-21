/**
 * UI Atoms Library
 *
 * All components are built with inline styles and ONLY use theme variables from `src/index.css`.
 * Import your app's `index.css` once at the root (already done in `main.tsx`).
 *
 * Usage Examples
 * ----------------
 *
 * Button variants and sizes:
 * import { Button } from "./ui";
 *
 * function ExampleButtons() {
 *   return (
 *     <div style={{ display: "flex", gap: "var(--spacing-lg)" }}>
 *       <Button>Primary</Button>
 *       <Button variant="secondary">Secondary</Button>
 *       <Button variant="outline">Outline</Button>
 *       <Button variant="ghost">Ghost</Button>
 *       <Button variant="danger">Danger</Button>
 *       <Button size="sm">Small</Button>
 *       <Button size="lg">Large</Button>
 *     </div>
 *   );
 * }
 *
 * Text sizes and colors:
 * import { Text } from "./ui";
 *
 * function ExampleText() {
 *   return (
 *     <div>
 *       <Text size="2xl" weight={600}>Heading</Text>
 *       <Text size="lg" color="neutral-700">Subtitle</Text>
 *       <Text size="sm" color="neutral-500">Caption</Text>
 *       <Text color="primary-600">Accent</Text>
 *     </div>
 *   );
 * }
 *
 * Input with label, helper and error:
 * import { Input } from "./ui";
 *
 * function ExampleInput() {
 *   return (
 *     <div style={{ maxWidth: 400 }}>
 *       <Input label="Email" name="email" placeholder="you@example.com" helperText="We'll never share your email." fullWidth />
 *       <div style={{ height: "var(--spacing-lg)" }} />
 *       <Input label="Username" name="username" error="Username is required" fullWidth />
 *     </div>
 *   );
 * }
 *
 * SearchBar controlled and uncontrolled usage:
 * import { SearchBar } from "./ui";
 *
 * function ExampleSearchBar() {
 *   const [q, setQ] = useState("");
 *   return (
 *     <>
 *       // Uncontrolled: manages its own state
 *       <SearchBar onSearch={(val) => console.log("search:", val)} fullWidth />
 *
 *       // Controlled: parent manages value
 *       <SearchBar value={q} onChange={setQ} onSearch={(val) => console.log("search:", val)} />
 *     </>
 *   );
 * }
 */

export { Button } from "./Button";
export type { ButtonProps, ButtonVariant, ButtonSize } from "./Button";

export { Text } from "./Text";
export type { TextProps, TextSize, TextWeight } from "./Text";

export { Input } from "./Input";
export type { InputProps } from "./Input";

export { SearchBar } from "./SearchBar";
export type { SearchBarProps } from "./SearchBar";

// New atoms
export { Label } from "./Label";
export type { LabelProps } from "./Label";

export { Textarea } from "./Textarea";
export type { TextareaProps } from "./Textarea";

export { Select } from "./Select";
export type { SelectProps, SelectOption } from "./Select";

export { Checkbox } from "./Checkbox";
export type { CheckboxProps } from "./Checkbox";

export { Radio } from "./Radio";
export type { RadioProps } from "./Radio";

export { Switch } from "./Switch";
export type { SwitchProps } from "./Switch";

export { Badge } from "./Badge";
export type { BadgeProps, BadgeVariant } from "./Badge";

export { Spinner } from "./Spinner";
export type { SpinnerProps } from "./Spinner";

export { Divider } from "./Divider";

export { Link } from "./Link";
export type { LinkProps } from "./Link";

export { Stack } from "./Stack";
export type { StackProps } from "./Stack";

export { Inline } from "./Inline";
export type { InlineProps } from "./Inline";

// Utilities
export { toast } from "./toast";

// Layout and containers
export { Panel } from "./Panel";
export type { PanelProps } from "./Panel";

export { SidebarContainer, SidebarItem } from "./Sidebar";
export type { SidebarContainerProps, SidebarItemProps } from "./Sidebar";

export { Grid } from "./Grid";
export type { GridProps } from "./Grid";

export { AppShell } from "./AppShell";
export type { AppShellProps } from "./AppShell";
