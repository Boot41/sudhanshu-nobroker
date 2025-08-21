import React, { useState } from "react";
import { Stack, Text, Button, Link as UILink, Divider, toast } from "../ui";
import { authStore } from "../store/authstore";
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
  // Local state only used when external handlers are not provided
  const [localSignupSubmitting, setLocalSignupSubmitting] = useState(false);
  const [localLoginSubmitting, setLocalLoginSubmitting] = useState(false);
  const [localSignupError, setLocalSignupError] = useState<string | undefined>(undefined);
  const [localLoginError, setLocalLoginError] = useState<string | undefined>(undefined);

  const handleSignupSubmit = async (vals: SignUpFormValues) => {
    if (onSignupSubmit) return onSignupSubmit(vals);
    try {
      setLocalSignupError(undefined);
      setLocalSignupSubmitting(true);
      await authStore.register({
        name: vals.name,
        email: vals.email,
        phone: vals.phone,
        password: vals.password,
        user_type: vals.user_type,
      });
      toast.success("Account created successfully");
      setMode("login");
    } catch (e: any) {
      setLocalSignupError(e?.message || "Unable to create account");
    } finally {
      setLocalSignupSubmitting(false);
    }
  };

  const handleLoginSubmit = async (vals: LoginFormValues) => {
    if (onLoginSubmit) return onLoginSubmit(vals);
    try {
      setLocalLoginError(undefined);
      setLocalLoginSubmitting(true);
      await authStore.login({
        email: vals.email,
        password: vals.password,
      });
      toast.success("Logged in successfully");
      // Navigate to owner dashboard after successful login
      if (typeof window !== "undefined") {
        // Keep it simple since we don't use a router: switch pathname
        window.location.assign("/owner");
      }
    } catch (e: any) {
      setLocalLoginError(e?.message || "Login failed");
    } finally {
      setLocalLoginSubmitting(false);
    }
  };

  const goBack = () => setMode("default");

  const containerStyle: React.CSSProperties = {
    width: "25%",
    minWidth: 320,
    height: "100vh",
    padding: "var(--spacing-2xl)",
    boxSizing: "border-box",
    borderRight: "1px solid var(--color-neutral-200)",
    background: "var(--color-neutral-50)",
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
            <Text as="p" size="md" color="neutral-700" style={{ marginTop: "var(--spacing-sm)", lineHeight: 1.5 }}>
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
          <Text as="h2" size="xl" weight={600} style={{ marginBottom: "var(--spacing-lg)" }}>
            Create your account
          </Text>
          <SignUpForm
            onSubmit={handleSignupSubmit}
            submitting={onSignupSubmit ? signupSubmitting : localSignupSubmitting}
            error={onSignupSubmit ? signupError : localSignupError}
          />
        </div>
      )}

      {mode === "login" && (
        <div>
          <Text as="h2" size="xl" weight={600} style={{ marginBottom: "var(--spacing-lg)" }}>
            Welcome back
          </Text>
          <LoginForm
            onSubmit={handleLoginSubmit}
            submitting={onLoginSubmit ? loginSubmitting : localLoginSubmitting}
            error={onLoginSubmit ? loginError : localLoginError}
          />
        </div>
      )}
    </aside>
  );
};

export default RegisterPanel;
