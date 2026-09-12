export const gestures = {
  Athe: { emoji: "👍", message: "Athe, manassilaayi." },
  Sheri: { emoji: "😌", message: "Sheri, set!" },
  Venda: { emoji: "❌", message: "Venda alle? 😭" },
  Nokkam: { emoji: "👀", message: "Nokkam..." },
  Ariyilla: { emoji: "🤷", message: "Enikkum ariyilla." },
} as const;

export type GestureName = keyof typeof gestures;
export type Prediction = {
  gesture: GestureName;
  confidence: number;
  message: string;
};

const pause = (milliseconds: number) =>
  new Promise((resolve) => window.setTimeout(resolve, milliseconds));

async function mockPrediction(): Promise<Prediction> {
  await pause(1450);
  const names = Object.keys(gestures) as GestureName[];
  const gesture = names[Math.floor(Math.random() * names.length)] ?? "Athe";
  const details = gestures[gesture];
  return {
    gesture,
    confidence: Number((0.8 + Math.random() * 0.18).toFixed(2)),
    message: details.message,
  };
}

export async function predictGesture(frame?: Blob): Promise<Prediction> {
  const apiUrl = import.meta.env["VITE_API_URL"] as string | undefined;
  if (!apiUrl) return mockPrediction();

  if (!frame) throw new Error("NO_FACE");
  const formData = new FormData();
  formData.append("image", frame, "nod-frame.jpg");
  const response = await fetch(`${apiUrl.replace(/\/$/, "")}/predict`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("BACKEND_ERROR");
  return (await response.json()) as Prediction;
}