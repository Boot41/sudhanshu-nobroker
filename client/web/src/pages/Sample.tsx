import React from "react";
import {
  Button,
  Text,
  Input,
  SearchBar,
  Label,
  Textarea,
  Select,
  Checkbox,
  Radio,
  Switch,
  Badge,
  Spinner,
  Divider,
  Link as UILink,
  Stack,
  Inline,
} from "../ui";
import SignUpForm from "../components/SignUpForm";
import LoginForm from "../components/LoginForm";
import RegisterPanel from "../components/RegisterPanel";
import DisplayCarousel from "../components/DisplayCarousel";

const Section: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, style, ...rest }) => (
  <section
    style={{
      margin: "var(--spacing-2xl) 0",
      ...style,
    }}
    {...rest}
  >
    {children}
  </section>
);

const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, style, ...rest }) => (
  <div
    style={{
      border: "1px solid var(--color-neutral-200)",
      padding: "var(--spacing-xl)",
      borderRadius: 8,
      background: "var(--color-neutral-50)",
      ...style,
    }}
    {...rest}
  >
    {children}
  </div>
);

const ColorSwatch: React.FC<{ name: string; token: string }> = ({ name, token }) => (
  <div style={{ width: 140 }}>
    <div
      style={{
        height: 40,
        background: `var(${token})`,
        border: "1px solid var(--color-neutral-200)",
        borderRadius: 6,
      }}
    />
    <Text size="sm" color="neutral-600">
      {name}
    </Text>
  </div>
);

const Sample: React.FC = () => {
  return (
    <div style={{ padding: "var(--spacing-3xl)", fontFamily: "var(--font-sans)", color: "var(--color-neutral-900)", background: "var(--color-neutral-50)" }}>
      <Text as="h1" size="3xl" weight={600}>
        UI Atoms Sample
      </Text>
      <Text color="neutral-600">A stateless page that renders all atoms and theme tokens.</Text>

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Display Carousel
        </Text>
        <DisplayCarousel />
        <Text size="sm" color="neutral-600">
          The marketing carousel auto-rotates through slides and spans full height. Controls are intentionally hidden.
        </Text>
      </Section>

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Register Panel
        </Text>
        <div style={{ display: "flex", gap: 24 }}>
          <RegisterPanel />
          <div style={{ flex: 1 }}>
            <Text size="md" color="neutral-700">
              This area represents the rest of the page content next to the panel.
            </Text>
          </div>
        </div>
      </Section>

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Buttons
        </Text>
        <Inline>
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="danger">Danger</Button>
        </Inline>
        <div style={{ height: "var(--spacing-lg)" }} />
        <Inline>
          <Button size="sm">Small</Button>
          <Button size="md">Medium</Button>
          <Button size="lg">Large</Button>
          <Button fullWidth style={{ maxWidth: 200 }}>
            Full width (200px container)
          </Button>
        </Inline>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Text
        </Text>
        <Stack>
          <Text size="2xl" weight={600}>Heading 2XL</Text>
          <Text size="xl" weight={600}>Heading XL</Text>
          <Text size="lg">Body Large</Text>
          <Text>Body</Text>
          <Text size="sm" color="neutral-600">Small Muted</Text>
          <Text color="primary-600">Primary Accent</Text>
          <Text color="secondary-600">Secondary Accent</Text>
        </Stack>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Form Elements
        </Text>
        <Card>
          <Stack>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" name="email" placeholder="you@example.com" fullWidth />
            </div>
            <div>
              <Label htmlFor="username">Username</Label>
              <Input id="username" name="username" error="Username is required" fullWidth />
            </div>
            <div>
              <Label htmlFor="about">About</Label>
              <Textarea id="about" name="about" placeholder="Tell us something..." fullWidth />
            </div>
            <div>
              <Label htmlFor="city">City</Label>
              <Select
                id="city"
                name="city"
                options={[
                  { label: "Bangalore", value: "blr" },
                  { label: "Mumbai", value: "bom" },
                  { label: "Pune", value: "pnq" },
                ]}
                fullWidth
              />
            </div>
            <Inline>
              <Checkbox label="Accept terms" defaultChecked />
              <Radio name="plan" value="basic" label="Basic" defaultChecked />
              <Radio name="plan" value="pro" label="Pro" />
              <Switch checked={true} onChange={() => {}} label="Notifications" />
            </Inline>
            <SearchBar onSearch={(v) => console.log("search", v)} fullWidth />
          </Stack>
        </Card>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Sign Up Form
        </Text>
        <Card>
          <div style={{ maxWidth: 520 }}>
            <SignUpForm onSubmit={(vals) => console.log("signup submit", vals)} />
          </div>
        </Card>
      </Section>

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Login Form
        </Text>
        <Card>
          <div style={{ maxWidth: 420 }}>
            <LoginForm onSubmit={(vals) => console.log("login submit", vals)} />
          </div>
        </Card>
      </Section>

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Badges, Spinner, Link
        </Text>
        <Inline>
          <Badge>Neutral</Badge>
          <Badge variant="primary">Primary</Badge>
          <Badge variant="secondary">Secondary</Badge>
          <Spinner />
          <Spinner color="secondary" />
          <UILink href="#">A Themed Link</UILink>
        </Inline>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Layout Helpers
        </Text>
        <Card>
          <Text weight={600}>Stack</Text>
          <Stack>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>A</div>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>B</div>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>C</div>
          </Stack>
          <div style={{ height: "var(--spacing-xl)" }} />
          <Text weight={600}>Inline</Text>
          <Inline>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>1</div>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>2</div>
            <div style={{ padding: "var(--spacing-md)", background: "var(--color-neutral-100)" }}>3</div>
          </Inline>
        </Card>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Theme Colors
        </Text>
        <Text size="sm" color="neutral-600">Pulled from CSS variables in src/index.css</Text>
        <div style={{ height: "var(--spacing-lg)" }} />
        <Stack>
          <Text weight={600}>Primary</Text>
          <Inline>
            {([50,100,200,300,400,500,600,700,800,900,950] as const).map((n) => (
              <ColorSwatch key={n} name={`primary-${n}`} token={`--color-primary-${n}`} />
            ))}
          </Inline>
          <Text weight={600}>Secondary</Text>
          <Inline>
            {([50,100,200,300,400,500,600,700,800,900,950] as const).map((n) => (
              <ColorSwatch key={n} name={`secondary-${n}`} token={`--color-secondary-${n}`} />
            ))}
          </Inline>
          <Text weight={600}>Neutral</Text>
          <Inline>
            {([50,100,200,300,400,500,600,700,800,900,950] as const).map((n) => (
              <ColorSwatch key={n} name={`neutral-${n}`} token={`--color-neutral-${n}`} />
            ))}
          </Inline>
        </Stack>
      </Section>

      <Divider />

      <Section>
        <Text as="h2" size="xl" weight={600}>
          Fonts
        </Text>
        <Stack>
          <div style={{ fontFamily: "var(--font-sans)" }}>
            <Text weight={600}>Sans</Text>
            <Text size="lg">The quick brown fox jumps over the lazy dog 1234567890</Text>
          </div>
          <div style={{ fontFamily: "var(--font-serif)" }}>
            <Text weight={600}>Serif</Text>
            <Text size="lg">The quick brown fox jumps over the lazy dog 1234567890</Text>
          </div>
          <div style={{ fontFamily: "var(--font-mono)" }}>
            <Text weight={600}>Mono</Text>
            <Text size="lg">The quick brown fox jumps over the lazy dog 1234567890</Text>
          </div>
        </Stack>
      </Section>
    </div>
  );
};

export default Sample;
