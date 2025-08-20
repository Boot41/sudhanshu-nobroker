import React, { useState } from "react";
import {
  Stack,
  Label,
  Input,
  Select,
  Button,
  Text,
} from "../ui";

export type UserType = "tenant" | "owner";

export interface SignUpFormValues {
  name: string;
  email: string;
  phone: string;
  password: string;
  user_type: UserType;
}

export interface SignUpFormProps {
  defaultValues?: Partial<SignUpFormValues>;
  submitting?: boolean;
  error?: string;
  onSubmit: (values: SignUpFormValues) => void;
}

const initialValues: SignUpFormValues = {
  name: "",
  email: "",
  phone: "",
  password: "",
  user_type: "tenant",
};

export const SignUpForm: React.FC<SignUpFormProps> = ({
  defaultValues,
  submitting,
  error,
  onSubmit,
}) => {
  const [values, setValues] = useState<SignUpFormValues>({
    ...initialValues,
    ...defaultValues,
  });

  const setField = (key: keyof SignUpFormValues, val: string) => {
    setValues((v) => ({ ...v, [key]: val } as SignUpFormValues));
  };

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    // Basic front-end checks (email format handled by input type)
    if (!values.name || !values.email || !values.phone || !values.password) {
      alert("Please fill in all required fields.");
      return;
    }
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} style={{ width: "100%" }}>
      <Stack gap="xl">
        <div>
          <Label htmlFor="name" requiredMark>
            Name
          </Label>
          <Input
            id="name"
            name="name"
            placeholder="Your full name"
            value={values.name}
            onChange={(e) => setField("name", e.target.value)}
            fullWidth
            required
          />
        </div>

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
          <Label htmlFor="phone" requiredMark>
            Phone
          </Label>
          <Input
            id="phone"
            name="phone"
            inputMode="tel"
            placeholder="e.g. +91 98765 43210"
            value={values.phone}
            onChange={(e) => setField("phone", e.target.value)}
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

        <div>
          <Label htmlFor="user_type" requiredMark>
            User Type
          </Label>
          <Select
            id="user_type"
            name="user_type"
            value={values.user_type}
            onChange={(e) => setField("user_type", e.target.value)}
            options={[
              { label: "Owner", value: "owner" },
              { label: "Tenant", value: "tenant" },
            ]}
            fullWidth
            required
          />
        </div>

        {error ? (
          <Text size="sm" color="primary-600">
            {error}
          </Text>
        ) : null}

        <div>
          <Button type="submit" variant="primary" disabled={submitting}>
            {submitting ? "Creating account..." : "Create account"}
          </Button>
        </div>
      </Stack>
    </form>
  );
};

export default SignUpForm;
