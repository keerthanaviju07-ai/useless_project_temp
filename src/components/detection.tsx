import { useCallback, useEffect, useRef, useState } from "react";
import { Camera, CameraOff, RefreshCw, ScanFace, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DecorativeSticker, DoodleStar } from "./decorative";
import { gestures, predictGesture, type Prediction } from "@/services/api";

type DetectionPhase = "waiting" | "detecting" | "analyzing" | "result" | "error";
type CameraProblem = "permission" | "missing" | "backend" | "no-face";

const wait = (milliseconds: number) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));

export function CameraView({ active, videoRef }: { active: boolean; videoRef: React.RefObject<HTMLVideoElement | null> }) {
  return (
    <div className={active ? "camera-screen camera-active" : "camera-screen"}>
      <video ref={videoRef} autoPlay muted playsInline aria-label="Live webcam preview" />
      {!active && <div className="camera-placeholder"><Camera /><span>CAMERA STANDBY</span><small>your face goes here</small></div>}
      <div className="viewfinder"><i /><i /><i /><i /></div>
      {active && <div className="scan-line" />}
      <span className="camera-time">REC • 00:0{active ? "3" : "0"}</span>
    </div>
  );
}

export function DetectionStatus({ phase }: { phase: DetectionPhase }) {
  const content = {
    waiting: ["READY?", "Position your face inside the frame."],
    detecting: ["LOOKING FOR A NOD...", "Keep your head in the little box."],
    analyzing: ["DECODING THE NOD...", "AI is thinking... please wait..."],
    result: ["RESULT INCOMING!", "The machine has made a decision."],
    error: ["UH-OH!", "Our tiny machine needs attention."],
  }[phase];
  return <div className="detection-status" aria-live="polite"><span>{phase === "detecting" ? "● AI WATCHING" : "NOD ANALYSIS SYSTEM"}</span><h2>{content[0]}</h2><p>{content[1]}</p>{phase === "analyzing" && <div className="thinking-dots"><i /><i /><i /></div>}</div>;
}

export function ConfidenceMeter({ value }: { value: number }) {
  const percentage = Math.round(value * 100);
  return <div className="confidence"><div><span>CONFIDENCE</span><strong>{percentage}%</strong></div><div className="confidence-track"><i style={{ width: `${percentage}%` }} /></div><small>surprisingly confident, honestly</small></div>;
}

export function ResultCard({ result, onReset }: { result: Prediction; onReset: () => void }) {
  const details = gestures[result.gesture];
  return (
    <div className="result-card">
      <span className="tape tape-center" /><DoodleStar className="result-star" />
      <span className="result-overline">YOUR NOD SAYS...</span>
      <h2>{result.gesture.toUpperCase()} <span>{details.emoji}</span></h2>
      <p>{result.message}</p><ConfidenceMeter value={result.confidence} />
      <p className="font-hand text-xl">“AI has spoken.”</p>
      <Button variant="hero" size="lg" onClick={onReset}><RefreshCw /> TRY AGAIN</Button>
    </div>
  );
}

export function ErrorState({ problem, onRetry }: { problem: CameraProblem; onRetry: () => void }) {
  const cameraProblem = problem === "permission" || problem === "missing";
  const copy = problem === "no-face"
    ? ["Where did you go? 👀", "Move into the camera frame."]
    : problem === "backend"
      ? ["AI is taking a tea break. ☕", "We couldn’t reach the Thalayattam engine."]
      : ["Oops. We can’t see you. 👀", problem === "missing" ? "We couldn’t find a camera on this device." : "Please allow camera access to use Thalayattam."];
  return <div className="error-note">{cameraProblem ? <CameraOff /> : <ScanFace />}<h2>{copy[0]}</h2><p>{copy[1]}</p><Button variant="scrap" size="lg" onClick={onRetry}><RefreshCw /> TRY AGAIN</Button></div>;
}

function captureFrame(video: HTMLVideoElement | null): Promise<Blob | undefined> {
  if (!video || video.videoWidth === 0) return Promise.resolve(undefined);
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth; canvas.height = video.videoHeight;
  canvas.getContext("2d")?.drawImage(video, 0, 0);
  return new Promise((resolve) => canvas.toBlob((blob) => resolve(blob ?? undefined), "image/jpeg", 0.82));
}

export function DetectionMachine() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [phase, setPhase] = useState<DetectionPhase>("waiting");
  const [problem, setProblem] = useState<CameraProblem>("permission");
  const [result, setResult] = useState<Prediction | null>(null);
  const [cameraReady, setCameraReady] = useState(false);

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null; setCameraReady(false);
  }, []);
  useEffect(() => stopCamera, [stopCamera]);

  const begin = async () => {
    setResult(null);
    if (!navigator.mediaDevices?.getUserMedia) { setProblem("missing"); setPhase("error"); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 } }, audio: false });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
      setCameraReady(true); setPhase("detecting");
      await wait(1800); setPhase("analyzing");
      const frame = await captureFrame(videoRef.current);
      const prediction = await predictGesture(frame);
      setResult(prediction); setPhase("result"); stopCamera();
    } catch (error) {
      stopCamera();
      const name = error instanceof DOMException ? error.name : "";
      setProblem(name === "NotFoundError" ? "missing" : error instanceof Error && error.message === "NO_FACE" ? "no-face" : error instanceof Error && error.message === "BACKEND_ERROR" ? "backend" : "permission");
      setPhase("error");
    }
  };
  const reset = () => { stopCamera(); setResult(null); setPhase("waiting"); };

  return (
    <main className="detect-page">
      <div className="detect-heading"><span className="kicker">WELCOME TO THE MACHINE</span><h1>SHOW US YOUR NOD</h1><p>Give us a nod... any nod.</p></div>
      <div className="detector-layout">
        <div className="webcam-rig">
          <DecorativeSticker tone="olive" className="absolute -left-4 top-8 -rotate-6 z-10">WEBCAM ONLINE</DecorativeSticker>
          <DecorativeSticker tone="pink" className="absolute -right-5 bottom-14 rotate-6 z-10">AI WATCHING 👀</DecorativeSticker>
          <div className="rig-bar"><span>NOD DETECTOR v1.0</span><span>_ □ ×</span></div>
          <CameraView active={cameraReady && (phase === "detecting" || phase === "analyzing")} videoRef={videoRef} />
          <div className="rig-footer"><span><i /> SYSTEM READY</span><span>DECODING MALAYALI</span></div>
        </div>
        <aside className="detector-panel">
          {phase === "result" && result ? <ResultCard result={result} onReset={reset} /> : phase === "error" ? <ErrorState problem={problem} onRetry={begin} /> : <>
            <DetectionStatus phase={phase} />
            {phase === "waiting" && <Button variant="hero" size="xl" onClick={begin}><Camera /> START DETECTION</Button>}
            {phase === "detecting" && <div className="activity-label"><i /> DO NOT SHAKE TOO HARD</div>}
            {phase === "analyzing" && <div className="analysis-ticket"><Sparkles /> THIS IS IMPORTANT RESEARCH</div>}
          </>}
        </aside>
      </div>
      <p className="responsible-note">PLEASE NOD RESPONSIBLY ↑</p>
    </main>
  );
}