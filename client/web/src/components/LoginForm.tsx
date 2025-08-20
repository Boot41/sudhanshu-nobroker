import React, { useState } from "react";
import { Stack, Label, Input, Button, Text } from "../ui";

export interface LoginFormValues {
  email: string;
  password: string;
}

export interface LoginFormProps {
  defaultValues?: Partial<LoginFormValues>;
  submitting?: boolean;
  error?: string;
  onSubmit: (values: LoginFormValues) => void;
}

const initialValues: LoginFormValues = {
  email: "",
  password: "",
};

export const LoginForm: React.FC<LoginFormProps> = ({
  defaultValues,
  submitting,
  error,
  onSubmit,
}) => {
  const [values, setValues] = useState<LoginFormValues>({
    ...initialValues,
    ...defaultValues,
  });

  const setField = (key: keyof LoginFormValues, val: string) => {
    setValues((v) => ({ ...v, [key]: val } as LoginFormValues));
  };

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    if (!values.email || !values.password) {
      alert("Please fill in both email and password.");
      return;
    }
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} style={{ width: "100%" }}>
      <Stack gap="xl">
        <div>
          <Label htmlFor="email" requiredMark>
            Email
          </Label>
          <Input
            id="email"
            name="email"
            type="email"
            placeholder="you@example.com"
            value={values.email}
            onChange={(e) => setField("email", e.target.value)}
            fullWidth
            required
          />
        </div>
        <div>
          <Label htmlFor="password" requiredMark>
            Password
          </Label>
          <Input
            id="password"
            name="password"
            type="password"
            placeholder="••••••••"
            value={values.password}
            onChange={(e) => setField("password", e.target.value)}
            fullWidth
            required
          />
        </div>
        {error ? (
          <Text size="sm" color="primary-600" style={{ marginTop: "var(--spacing-xs)" }}>
            {error}
          </Text>
        ) : null}
        <div>
          <Button type="submit" variant="primary" disabled={submitting} fullWidth>
            {submitting ? "Logging in..." : "Log in"}
          </Button>
        </div>
      </Stack>
    </form>
  );
};

export default LoginForm;
