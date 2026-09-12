import { createFileRoute } from "@tanstack/react-router";
import { DetectionMachine } from "@/components/detection";

export const Route = createFileRoute("/detect")({
  head: () => ({ meta: [
    { title: "Try the Nod Detector — Thalayattam" },
    { name: "description", content: "Show the webcam your best Malayali nod and let our playful AI interpret it." },
    { property: "og:title", content: "Try the Thalayattam Nod Detector" },
    { property: "og:description", content: "Give us a nod—any nod—and discover what it says." },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
  ]}),
  component: DetectionMachine,
});