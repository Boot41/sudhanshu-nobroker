import React, { useState } from "react";
import { Stack, Text, Button, Link as UILink, Divider } from "../ui";
import SignUpForm, { type SignUpFormValues } from "./SignUpForm";
import LoginForm, { type LoginFormValues } from "./LoginForm";

export interface RegisterPanelProps {
  onSignupSubmit?: (values: SignUpFormValues) => void;
  onLoginSubmit?: (values: LoginFormValues) => void;
  signupSubmitting?: boolean;
  loginSubmitting?: boolean;
  signupError?: string;
  loginError?: string;
  title?: string;
  tagline?: string;
}

/**
 * A vertical panel that takes 1/4th page width and full viewport height.
 * Shows app title, tagline and CTA buttons. Clicking CTA opens inline forms.
 * Uses only components exported from ../ui for layout/typography/buttons/links.
 */
const RegisterPanel: React.FC<RegisterPanelProps> = ({
  onSignupSubmit,
  onLoginSubmit,
  signupSubmitting,
  loginSubmitting,
  signupError,
  loginError,
  title = "NoBroker Clone",
  tagline = "Get rid of unreasonable brokerage, join us",
}) => {
  const [mode, setMode] = useState<"default" | "signup" | "login">("default");

  const goBack = () => setMode("default");

  const containerStyle: React.CSSProperties = {
    width: "25%",
    minWidth: 280,
    height: "100vh",
    padding: "var(--spacing-xl)",
    boxSizing: "border-box",
    borderRight: "1px solid var(--color-neutral-200)",
    overflowY: "auto",
  };

  return (
    <aside style={containerStyle}>
      {mode !== "default" ? (
        <div style={{ marginBottom: "var(--spacing-md)" }}>
          <UILink href="#" onClick={(e) => { e.preventDefault(); goBack(); }}>
            ← Back
          </UILink>
        </div>
      ) : null}

      {mode === "default" && (
        <Stack gap="xl">
          <div>
            <Text as="h1" size="2xl" weight={700}>
              {title}
            </Text>
            <Text as="p" size="md" color="neutral-700">
              {tagline}
            </Text>
          </div>

          <Divider />

          <Stack gap="md">
            <Button variant="primary" onClick={() => setMode("signup")} fullWidth>
              Sign Up
            </Button>
            <Button variant="secondary" onClick={() => setMode("login")} fullWidth>
              Log In
            </Button>
          </Stack>
        </Stack>
      )}

      {mode === "signup" && (
        <div>
          <Text as="h2" size="xl" weight={600} style={{ marginBottom: "var(--spacing-md)" }}>
            Create your account
          </Text>
          <SignUpForm
            onSubmit={(vals) => onSignupSubmit ? onSignupSubmit(vals) : console.log("signup", vals)}
            submitting={signupSubmitting}
            error={signupError}
          />
        </div>
      )}

      {mode === "login" && (
        <div>
          <Text as="h2" size="xl" weight={600} style={{ marginBottom: "var(--spacing-md)" }}>
            Welcome back
          </Text>
          <LoginForm
            onSubmit={(vals) => onLoginSubmit ? onLoginSubmit(vals) : console.log("login", vals)}
            submitting={loginSubmitting}
            error={loginError}
          />
        </div>
      )}
    </aside>
  );
};

export default RegisterPanel;
