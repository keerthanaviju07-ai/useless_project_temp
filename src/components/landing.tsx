import { Link } from "@tanstack/react-router";
import { Camera, Cpu, ScanFace, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DecorativeSticker, DoodleStar, HandDrawnArrow } from "./decorative";

export function RetroComputer() {
  return (
    <div className="computer-wrap" aria-label="Illustration of a retro computer recognizing a nod">
      <div className="computer-camera"><span /></div>
      <div className="computer-shell">
        <div className="computer-topline"><span>THALAYATTAM_CAM.EXE</span><span>×</span></div>
        <div className="computer-screen">
          <div className="scan-corners" />
          <div className="pixel-face"><span className="eye left" /><span className="eye right" /><span className="nose" /><span className="smile" /></div>
          <div className="screen-status"><i /> HEAD DETECTED</div>
        </div>
        <div className="computer-controls"><span /><span /><small>NOD MODE: ON</small></div>
      </div>
      <div className="computer-stand" />
      <DecorativeSticker tone="pink" className="absolute -right-7 top-14 rotate-6">VERY SERIOUS AI</DecorativeSticker>
      <DecorativeSticker tone="yellow" className="absolute -left-8 bottom-24 -rotate-6">100% SCIENTIFIC*</DecorativeSticker>
    </div>
  );
}

export function Hero() {
  return (
    <section className="hero-section">
      <DoodleStar className="absolute left-[4%] top-16 w-12 text-accent" />
      <div className="hero-copy">
        <div className="eyebrow"><span>★</span> AI COMPUTER VISION, BUT MAKE IT MALLU</div>
        <h1>WHAT DID YOUR <span>NOD</span> SAY?</h1>
        <p className="hero-subtitle">An AI that understands the unspoken language of the Malayali nod.</p>
        <p className="font-hand text-xl">“Because apparently, even a nod needs technology.”</p>
        <div className="hero-actions">
          <Button asChild variant="hero" size="xl"><Link to="/detect">TRY THALAYATTAM <span aria-hidden="true">→</span></Link></Button>
          <small>AI-powered • Camera-based • Slightly unnecessary</small>
        </div>
      </div>
      <div className="hero-machine">
        <RetroComputer />
        <div className="process-note"><span>HEAD</span><b>↓</b><span>AI</span><b>↓</b><span>WHAT DID IT MEAN?</span></div>
        <p className="scribble-note">please nod responsibly ↗</p>
      </div>
    </section>
  );
}

const steps = [
  { number: "01", label: "STEP ONE", title: "LOOK", copy: "Face the camera.", icon: Camera },
  { number: "02", label: "STEP TWO", title: "NOD", copy: "Give us your best Malayali head movement.", icon: ScanFace },
  { number: "03", label: "THE IMPORTANT PART", title: "DISCOVER", copy: "Let AI interpret what you really meant.", icon: Sparkles },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="section-block grid-paper">
      <div className="section-heading"><span className="kicker">THE PROCESS.TXT</span><h2>HOW DOES THIS THING EVEN WORK?</h2></div>
      <div className="steps-row">
        {steps.map(({ number, label, title, copy, icon: Icon }, index) => (
          <div className={`step-card step-${index + 1}`} key={title}>
            <span className="step-number">{number}</span><span className="note-label">{label}</span>
            <Icon aria-hidden="true" /><h3>{title}</h3><p>{copy}</p>
            {index < 2 && <HandDrawnArrow className="step-arrow" />}
          </div>
        ))}
      </div>
      <p className="font-hand text-center text-xl">science is happening somewhere around step 03 ↑</p>
    </section>
  );
}

const nods = [
  { malayalam: "അതെ", name: "ATHE", english: "YES", copy: "Athe, manassilaayi. 👍", tone: "pink", note: "CONFIRMED!" },
  { malayalam: "ശരി", name: "SHERI", english: "OKAY", copy: "Sheri, set! 😌", tone: "blue", note: "ALL SET" },
  { malayalam: "വേണ്ട", name: "VENDA", english: "NO", copy: "Venda alle? ❌", tone: "yellow", note: "ABSOLUTELY NOT" },
  { malayalam: "നോക്കാം", name: "NOKKAM", english: "LET'S SEE", copy: "Nokkam... 👀", tone: "orange", note: "CLASSIC" },
  { malayalam: "അറിയില്ല", name: "ARIYILLA", english: "DON'T KNOW", copy: "Enikkum ariyilla. 🤷", tone: "olive", note: "HONEST" },
];

export function GestureCard({ nod, index }: { nod: (typeof nods)[number]; index: number }) {
  return (
    <article className={`gesture-card gesture-${index + 1}`}>
      <span className={`gesture-tab tab-${nod.tone}`}>{nod.note}</span>
      <span className="malayalam">{nod.malayalam}</span>
      <p className="gesture-index">0{index + 1} / NOD</p><h3>{nod.name}</h3><strong>{nod.english}</strong><p>{nod.copy}</p>
      <span className="card-doodle" aria-hidden="true">{index % 2 ? "✿" : "✦"}</span>
    </article>
  );
}

export function GestureDictionary() {
  return (
    <section id="the-nods" className="section-block dictionary-section">
      <div className="section-heading left"><span className="kicker">A FIELD GUIDE</span><h2>THE MALAYALI<br />NOD DICTIONARY</h2><p className="font-hand">five tiny movements. infinite confusion.</p></div>
      <div className="gesture-grid">{nods.map((nod, index) => <GestureCard nod={nod} index={index} key={nod.name} />)}</div>
    </section>
  );
}

export function WhySection() {
  return (
    <section className="why-section">
      <div className="why-note">
        <span className="tape tape-left" /><span className="tape tape-right" />
        <div className="why-title"><span>RESEARCH LOG #001</span><h2>WHY?</h2></div>
        <div className="why-copy"><p>We wanted to teach a computer one of the most mysterious forms of human communication:</p><strong>THE MALAYALI HEAD NOD.</strong></div>
        <div className="question-list"><p>Is it yes?</p><p>Is it no?</p><p>Is it maybe?</p><p>Is it “let’s see”?</p><b>Now AI has to figure it out.</b></div>
        <div className="margin-notes"><span>THIS IS IMPORTANT RESEARCH.</span><span>VERY SERIOUS.</span><span>PROBABLY.</span><span>DO NOT QUESTION THE SCIENCE.</span></div>
        <Cpu className="why-chip" aria-hidden="true" />
      </div>
    </section>
  );
}

export function HomePage() {
  return <main><Hero /><HowItWorks /><GestureDictionary /><WhySection /></main>;
}