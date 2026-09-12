import { createFileRoute } from "@tanstack/react-router";
import { HomePage } from "@/components/landing";

export const Route = createFileRoute("/")({
  head: () => ({ meta: [
    { title: "Thalayattam Technologies — What Did Your Nod Say?" },
    { name: "description", content: "A playful AI experiment decoding the unspoken language of the Malayali head nod." },
    { property: "og:title", content: "Thalayattam Technologies" },
    { property: "og:description", content: "What did your nod say? Let AI decode your Malayali head movement." },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
  ]}),
  component: HomePage,
});
