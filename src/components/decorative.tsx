import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function DecorativeSticker({
  children,
  tone = "yellow",
  className,
}: {
  children: ReactNode;
  tone?: "yellow" | "pink" | "blue" | "olive";
  className?: string;
}) {
  const tones = {
    yellow: "bg-sticker-yellow",
    pink: "bg-sticker-pink",
    blue: "bg-sticker-blue",
    olive: "bg-primary text-primary-foreground",
  };
  return (
    <span className={cn("sticker", tones[tone], className)}>{children}</span>
  );
}

export function DoodleStar({ className }: { className?: string }) {
  return (
    <svg className={cn("doodle-star", className)} viewBox="0 0 64 64" aria-hidden="true">
      <path d="M31 3c2 19 7 25 28 28-20 3-26 9-28 30C28 40 22 34 3 31 22 28 28 22 31 3Z" />
    </svg>
  );
}

export function HandDrawnArrow({ className }: { className?: string }) {
  return (
    <svg className={cn("doodle-arrow", className)} viewBox="0 0 130 60" aria-hidden="true">
      <path d="M4 18c34 29 75 29 115 7M101 12l19 13-18 12" />
    </svg>
  );
}