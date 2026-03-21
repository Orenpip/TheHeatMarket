import { requireStudent } from "@/lib/auth";
import MapCanvas from "@/components/map/MapCanvas";

// Minimal wrapper page for embedding the map in the mobile WebView.
// No nav, no padding — just the raw canvas.
export default async function MapEmbedPage() {
  await requireStudent();

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "#F2F4F7",
        overflow: "hidden",
      }}
    >
      <MapCanvas />
    </div>
  );
}
