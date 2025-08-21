import React, { useEffect, useState } from "react";
import { AppShell, Panel, Stack, Text, Label, Input, Textarea, Button, toast } from "../ui";
import OwnerSidebar from "../components/owner/OwnerSidebar";
import { authStore } from "../store/authstore";
import { propertyStore } from "../store/propertystore";
import type { PropertyCreate } from "../api";

const initialValues: PropertyCreate = {
  name: "",
  address: "",
  city: "",
  state: "",
  pincode: "",
  price: 0,
  bedrooms: 1,
  bathrooms: 1,
  area_sqft: 0,
  description: "",
};

const PostProperty: React.FC = () => {
  const [values, setValues] = useState<PropertyCreate>(initialValues);
  const [submitting, setSubmitting] = useState(false);

  // Auth guard: redirect to /home if no token
  useEffect(() => {
    const { token } = authStore.getState();
    if (!token && typeof window !== "undefined") {
      toast.error("Please log in as owner to post a property");
      window.location.assign("/home");
    }
  }, []);

  const onChange = (key: keyof PropertyCreate, val: string) => {
    setValues((v) => {
      const next: any = { ...v };
      if (["price", "bedrooms", "bathrooms", "area_sqft"].includes(key as string)) {
        // Numeric fields
        if (key === "price") next[key] = Number(val);
        else next[key] = parseInt(val || "0", 10);
      } else {
        next[key] = val;
      }
      return next;
    });
  };

  const validate = (): string | null => {
    if (!values.name || !values.address || !values.city || !values.state || !values.pincode) return "All fields except description are required";
    if (!/^[0-9]{5,6}$/.test(values.pincode)) return "Pincode should be 5-6 digits";
    if (values.price <= 0) return "Price must be greater than 0";
    if (values.bedrooms < 0 || values.bathrooms < 0 || values.area_sqft <= 0) return "Invalid room/area inputs";
    return null;
  };

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    const err = validate();
    if (err) {
      toast.error(err);
      return;
    }
    try {
      setSubmitting(true);
      await propertyStore.createProperty({ ...values, description: values.description || undefined });
      toast.success("Property posted successfully");
      if (typeof window !== "undefined") window.location.assign("/owner");
    } catch (er: any) {
      toast.error(er?.message || "Failed to post property");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppShell sidebar={<OwnerSidebar selected="properties" onSelect={() => {}} /> }>
      <Panel padding={24} radius={12} shadow>
        <Stack gap="lg">
          <Text size="xl" weight={700}>Post new property</Text>
          <form onSubmit={handleSubmit} style={{ width: "100%" }}>
            <Stack gap="md">
              <div>
                <Label htmlFor="name" requiredMark>Name</Label>
                <Input id="name" name="name" value={values.name} onChange={(e) => onChange("name", e.target.value)} fullWidth required />
              </div>

              <div>
                <Label htmlFor="address" requiredMark>Address</Label>
                <Textarea id="address" name="address" value={values.address} onChange={(e) => onChange("address", e.target.value)} fullWidth required />
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "var(--spacing-md)" }}>
                <div>
                  <Label htmlFor="city" requiredMark>City</Label>
                  <Input id="city" name="city" value={values.city} onChange={(e) => onChange("city", e.target.value)} fullWidth required />
                </div>
                <div>
                  <Label htmlFor="state" requiredMark>State</Label>
                  <Input id="state" name="state" value={values.state} onChange={(e) => onChange("state", e.target.value)} fullWidth required />
                </div>
                <div>
                  <Label htmlFor="pincode" requiredMark>Pincode</Label>
                  <Input id="pincode" name="pincode" value={values.pincode} onChange={(e) => onChange("pincode", e.target.value)} fullWidth required />
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: "var(--spacing-md)" }}>
                <div>
                  <Label htmlFor="price" requiredMark>Price (INR)</Label>
                  <Input id="price" name="price" type="number" min={0} value={String(values.price)} onChange={(e) => onChange("price", e.target.value)} fullWidth required />
                </div>
                <div>
                  <Label htmlFor="bedrooms" requiredMark>Bedrooms</Label>
                  <Input id="bedrooms" name="bedrooms" type="number" min={0} value={String(values.bedrooms)} onChange={(e) => onChange("bedrooms", e.target.value)} fullWidth required />
                </div>
                <div>
                  <Label htmlFor="bathrooms" requiredMark>Bathrooms</Label>
                  <Input id="bathrooms" name="bathrooms" type="number" min={0} value={String(values.bathrooms)} onChange={(e) => onChange("bathrooms", e.target.value)} fullWidth required />
                </div>
                <div>
                  <Label htmlFor="area_sqft" requiredMark>Area (sqft)</Label>
                  <Input id="area_sqft" name="area_sqft" type="number" min={0} value={String(values.area_sqft)} onChange={(e) => onChange("area_sqft", e.target.value)} fullWidth required />
                </div>
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea id="description" name="description" value={values.description || ""} onChange={(e) => onChange("description", e.target.value)} fullWidth />
              </div>

              <div>
                <Button type="submit" variant="primary" disabled={submitting} fullWidth>
                  {submitting ? "Posting..." : "Post property"}
                </Button>
              </div>
            </Stack>
          </form>
        </Stack>
      </Panel>
    </AppShell>
  );
};

export default PostProperty;
