import {
  AbsoluteFill,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  random,
} from "remotion";

// A 5-second, 30fps hero animation for the Rhody Strolls logo.
// Design intent (art direction):
//   - Open in near-black; suggest depth and the hush before a walk in the woods.
//   - A ring of light traces the circle first — an "iris" that promises what's inside.
//   - The logo settles in with a decisive spring, then breathes.
//   - Warm sunlight sweeps across the mark; dust motes drift; a soft red halo pulses.
//   - Vignette holds the eye; final beat lets the mark own the screen.

const LOGO_PATH = staticFile("logo.png");

const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  // Warm, slow parallax gradient — very subtle, never competes with the mark.
  const t = frame / durationInFrames;
  const hueA = interpolate(t, [0, 1], [18, 28]);
  const hueB = interpolate(t, [0, 1], [140, 130]);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(1200px 900px at 50% 55%,
            hsl(${hueA}, 30%, 12%) 0%,
            hsl(${hueB}, 25%, 6%) 55%,
            #000 100%)`,
      }}
    />
  );
};

const DustMotes: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const motes = new Array(48).fill(0).map((_, i) => {
    const seedX = random(`x${i}`);
    const seedY = random(`y${i}`);
    const seedS = random(`s${i}`);
    const seedD = random(`d${i}`);
    const drift = Math.sin((frame + i * 7) / 45) * 18;
    const x = seedX * width + drift;
    const y = ((seedY * height + frame * (0.3 + seedD * 0.7)) % height);
    const size = 1 + seedS * 3;
    const opacity = 0.12 + seedS * 0.35;
    return (
      <div
        key={i}
        style={{
          position: "absolute",
          left: x,
          top: y,
          width: size,
          height: size,
          borderRadius: "50%",
          background: "rgba(255, 236, 190, 1)",
          opacity,
          filter: `blur(${0.4 + seedS * 0.8}px)`,
          boxShadow: "0 0 6px rgba(255,220,160,0.7)",
        }}
      />
    );
  });
  return <AbsoluteFill>{motes}</AbsoluteFill>;
};

const IrisMask: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const open = spring({
    frame,
    fps,
    config: { damping: 22, mass: 0.9, stiffness: 90 },
    durationInFrames: 30,
  });
  const radius = interpolate(open, [0, 1], [0, Math.max(width, height) * 0.65]);
  const cx = width / 2;
  const cy = height / 2;
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        WebkitMaskImage: `radial-gradient(circle at ${cx}px ${cy}px, black ${radius}px, transparent ${radius + 24}px)`,
        maskImage: `radial-gradient(circle at ${cx}px ${cy}px, black ${radius}px, transparent ${radius + 24}px)`,
      }}
    >
      {children}
    </div>
  );
};

const LightSweep: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  // Sweep once around 3.0s, again subtly at 4.4s.
  const sweep1 = spring({ frame: frame - 90, fps, config: { damping: 200, stiffness: 80 }, durationInFrames: 30 });
  const sweep2 = spring({ frame: frame - 132, fps, config: { damping: 200, stiffness: 80 }, durationInFrames: 20 });
  const x1 = interpolate(sweep1, [0, 1], [-width * 0.5, width * 0.9]);
  const x2 = interpolate(sweep2, [0, 1], [-width * 0.5, width * 0.9]);
  const opacity1 = interpolate(frame, [90, 100, 115, 125], [0, 0.55, 0.55, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const opacity2 = interpolate(frame, [132, 140, 148, 150], [0, 0.28, 0.28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const beam = (x: number, opacity: number, w: number) => (
    <div
      style={{
        position: "absolute",
        top: -100,
        left: x,
        width: w,
        height: "140%",
        transform: "rotate(18deg)",
        background:
          "linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,240,200,0.8) 45%, rgba(255,255,255,0) 100%)",
        mixBlendMode: "screen",
        opacity,
        filter: "blur(6px)",
      }}
    />
  );
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {beam(x1, opacity1, 260)}
      {beam(x2, opacity2, 160)}
    </AbsoluteFill>
  );
};

const RedHalo: React.FC = () => {
  const frame = useCurrentFrame();
  // A subtle heartbeat pulse behind the ring, kicks in after the settle.
  const pulse = Math.sin(((frame - 60) / 30) * Math.PI * 2) * 0.5 + 0.5;
  const intensity = interpolate(frame, [55, 75], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const opacity = 0.15 + pulse * 0.18 * intensity;
  const scale = 1 + pulse * 0.015 * intensity;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", pointerEvents: "none" }}>
      <div
        style={{
          width: 900,
          height: 900,
          borderRadius: "50%",
          boxShadow: `0 0 120px 40px rgba(230, 40, 40, ${opacity})`,
          transform: `scale(${scale})`,
        }}
      />
    </AbsoluteFill>
  );
};

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.55) 85%, rgba(0,0,0,0.85) 100%)",
      pointerEvents: "none",
    }}
  />
);

const Logo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Entrance: spring from slightly enlarged + soft to settled.
  const enter = spring({
    frame: frame - 8,
    fps,
    config: { damping: 14, mass: 0.9, stiffness: 110 },
    durationInFrames: 45,
  });
  const scale = interpolate(enter, [0, 1], [1.18, 1.0]);
  const blur = interpolate(enter, [0, 1], [14, 0]);
  const opacity = interpolate(frame, [8, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Breathing after settle (very small; keeps the mark feeling alive without wobbling).
  const breathe = Math.sin((frame - 60) / 42) * 0.006;
  const settleScale = frame > 55 ? 1 + breathe : 1;

  // Micro Ken-Burns *inside* the entrance so it feels like the world is exhaling.
  const kb = interpolate(frame, [0, 150], [1.02, 1.0]);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          transform: `scale(${scale * settleScale * kb})`,
          filter: `blur(${blur}px) drop-shadow(0 20px 60px rgba(0,0,0,0.55))`,
          opacity,
          willChange: "transform, filter, opacity",
        }}
      >
        <Img
          src={LOGO_PATH}
          style={{
            width: 820,
            height: 820,
            objectFit: "contain",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const RhodyStrollsLogo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: "black" }}>
      <Backdrop />
      <Sequence from={0}>
        <IrisMask>
          <RedHalo />
          <Logo />
          <DustMotes />
          <LightSweep />
        </IrisMask>
      </Sequence>
      <Vignette />
    </AbsoluteFill>
  );
};
