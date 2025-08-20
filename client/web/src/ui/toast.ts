// Minimal toast utility (no dependency). Imperative API: toast.success/error/info
// Renders to a singleton container appended to document.body

export type ToastType = "success" | "error" | "info";

interface ToastOptions {
  duration?: number; // ms
}

let container: HTMLDivElement | null = null;

function ensureContainer() {
  if (typeof document === "undefined") return null;
  if (container) return container;
  container = document.createElement("div");
  container.setAttribute("data-toast-container", "");
  Object.assign(container.style, {
    position: "fixed",
    top: "16px",
    right: "16px",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    zIndex: 9999 as unknown as string,
    pointerEvents: "none",
  } as Partial<CSSStyleDeclaration>);
  document.body.appendChild(container);
  return container;
}

function show(message: string, type: ToastType, opts: ToastOptions = {}) {
  const root = ensureContainer();
  if (!root) return;
  const node = document.createElement("div");
  const bg =
    type === "success"
      ? "var(--color-primary-600)"
      : type === "error"
      ? "#dc2626"
      : "#374151";
  Object.assign(node.style, {
    background: bg,
    color: "white",
    padding: "10px 14px",
    borderRadius: "8px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
    fontFamily: "var(--font-sans)",
    fontSize: "14px",
    lineHeight: "1.3",
    pointerEvents: "auto",
  } as Partial<CSSStyleDeclaration>);
  node.textContent = message;
  root.appendChild(node);
  const duration = opts.duration ?? 2500;
  window.setTimeout(() => {
    node.style.transition = "opacity 200ms ease, transform 200ms ease";
    node.style.opacity = "0";
    node.style.transform = "translateY(-6px)";
    window.setTimeout(() => root.removeChild(node), 220);
  }, duration);
}

export const toast = {
  success: (msg: string, opts?: ToastOptions) => show(msg, "success", opts),
  error: (msg: string, opts?: ToastOptions) => show(msg, "error", opts),
  info: (msg: string, opts?: ToastOptions) => show(msg, "info", opts),
};

export default toast;
