import React, { useEffect, useMemo, useRef, useState } from "react";
import { AppShell, Stack, Text, Input, Textarea, Button, Inline, Label, Spinner } from "../ui";
import OwnerSidebar from "../components/owner/OwnerSidebar";
import type { OwnerTab } from "../components/owner/OwnerSidebar";
import { propertyStore } from "../store/propertystore";
import { authStore } from "../store/authstore";

const EditProperty: React.FC = () => {
  const [tab, setTab] = useState<OwnerTab>("properties");
  const [id, setId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const userClicked = useRef(false);

  // Form state: all optional
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [stateVal, setStateVal] = useState("");
  const [pincode, setPincode] = useState("");
  const [price, setPrice] = useState("");
  const [bedrooms, setBedrooms] = useState("");
  const [bathrooms, setBathrooms] = useState("");
  const [area, setArea] = useState("");
  const [description, setDescription] = useState("");

  // Auth guard + parse id
  useEffect(() => {
    const { token } = authStore.getState();
    if (!token && typeof window !== "undefined") {
      window.location.assign("/home");
      return;
    }
    if (typeof window !== "undefined") {
      const parts = window.location.pathname.split("/").filter(Boolean);
      const idx = parts.indexOf("property");
      const parsed = idx >= 0 ? Number(parts[idx + 1]) : NaN;
      if (!Number.isFinite(parsed) || parsed <= 0) {
        setError("Invalid property id");
        setLoading(false);
        return;
      }
      setId(parsed);
    }
  }, []);

  // Load current details for placeholders
  useEffect(() => {
    if (id == null) return;
    setLoading(true);
    propertyStore
      .fetchMineById(id)
      .then(() => setLoading(false))
      .catch((e) => {
        setError(e?.message || "Failed to load property");
        setLoading(false);
      });
  }, [id]);

  const current = useMemo(() => propertyStore.getState().current, [loading]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    try {
      const payload: any = {};
      if (name.trim()) payload.name = name.trim();
      if (address.trim()) payload.address = address.trim();
      if (city.trim()) payload.city = city.trim();
      if (stateVal.trim()) payload.state = stateVal.trim();
      if (pincode.trim()) payload.pincode = pincode.trim();
      if (price.trim()) payload.price = Number(price);
      if (bedrooms.trim()) payload.bedrooms = Number(bedrooms);
      if (bathrooms.trim()) payload.bathrooms = Number(bathrooms);
      if (area.trim()) payload.area_sqft = Number(area);
      if (description.trim()) payload.description = description.trim();

      if (Object.keys(payload).length === 0) {
        setError("Please change at least one field to update");
        return;
      }

      await propertyStore.updateProperty(id, payload);
      if (typeof window !== "undefined") window.location.assign(`/owner/property/${id}`);
    } catch (err: any) {
      setError(err?.message || "Update failed");
    }
  };

  // Sidebar actions: do not trigger on initial mount
  const didMount = useRef(false);
  useEffect(() => {
    if (!didMount.current) {
      didMount.current = true;
      return;
    }
    if (!userClicked.current) return; // only navigate when user explicitly clicked sidebar
    if (tab === "logout") {
      (async () => {
        await authStore.logoutAsync();
        if (typeof window !== "undefined") window.location.assign("/home");
      })();
    } else if (tab === "properties") {
      if (typeof window !== "undefined") window.location.assign("/owner");
    }
    userClicked.current = false; // reset after handling
  }, [tab]);

  return (
    <AppShell sidebar={<OwnerSidebar selected={tab} onSelect={(t) => { userClicked.current = true; setTab(t); }} />}>
      <Stack gap="lg">
        <Inline align="center" style={{ justifyContent: "space-between" }}>
          <Stack gap="xs">
            <Text size="2xl" weight={700}>Edit Property</Text>
            <Text color="neutral-600">Update one or more fields and save</Text>
          </Stack>
          {!loading && (
            <Button variant="secondary" onClick={() => typeof window !== "undefined" && id && window.location.assign(`/owner/property/${id}`)}>Cancel</Button>
          )}
        </Inline>

        {loading && (
          <Stack gap="sm" style={{ alignItems: "center" }}>
            <Spinner />
            <Text>Loading...</Text>
          </Stack>
        )}
        {error && !loading && (
          <Text color="neutral-700">{error}</Text>
        )}

        {!loading && current && (
          <form onSubmit={onSubmit}>
            <Stack gap="md">
              <Stack gap="xs">
                <Label htmlFor="name">Name</Label>
                <Input id="name" placeholder={current.name} value={name} onChange={(e) => setName(e.target.value)} />
              </Stack>

              <Stack gap="xs">
                <Label htmlFor="address">Address</Label>
                <Input id="address" placeholder={current.address} value={address} onChange={(e) => setAddress(e.target.value)} />
              </Stack>

              <Stack gap="xs">
                <Label htmlFor="city">City</Label>
                <Input id="city" placeholder={current.city} value={city} onChange={(e) => setCity(e.target.value)} />
              </Stack>

              <Stack gap="xs">
                <Label htmlFor="state">State</Label>
                <Input id="state" placeholder={current.state} value={stateVal} onChange={(e) => setStateVal(e.target.value)} />
              </Stack>

              <Stack gap="xs">
                <Label htmlFor="pincode">Pincode</Label>
                <Input id="pincode" placeholder={current.pincode} value={pincode} onChange={(e) => setPincode(e.target.value)} />
              </Stack>

              <Stack gap="xs">
                <Label htmlFor="price">Price</Label>
                <Input id="price" type="number" placeholder={String(current.price)} value={price} onChange={(e) => setPrice(e.target.value)} />
              </Stack>

              <Inline gap="md" wrap>
                <Stack gap="xs">
                  <Label htmlFor="bedrooms">Bedrooms</Label>
                  <Input id="bedrooms" type="number" placeholder={String(current.bedrooms)} value={bedrooms} onChange={(e) => setBedrooms(e.target.value)} />
                </Stack>
                <Stack gap="xs">
                  <Label htmlFor="bathrooms">Bathrooms</Label>
                  <Input id="bathrooms" type="number" placeholder={String(current.bathrooms)} value={bathrooms} onChange={(e) => setBathrooms(e.target.value)} />
                </Stack>
                <Stack gap="xs">
                  <Label htmlFor="area">Area (sqft)</Label>
                  <Input id="area" type="number" placeholder={String(current.area_sqft)} value={area} onChange={(e) => setArea(e.target.value)} />
                </Stack>
              </Inline>

              <Stack gap="xs">
                <Label htmlFor="desc">Description</Label>
                <Textarea id="desc" placeholder={current.description || ""} value={description} onChange={(e) => setDescription(e.target.value)} />
              </Stack>

              <Inline gap="sm" wrap={false}>
                <Button type="submit" variant="primary">Save Changes</Button>
              </Inline>
            </Stack>
          </form>
        )}
      </Stack>
    </AppShell>
  );
};

export default EditProperty;
