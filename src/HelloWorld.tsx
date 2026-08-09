import { AbsoluteFill, interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const scale = spring({ frame, fps, config: { damping: 12 } });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #6d28d9 100%)",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          textAlign: "center",
          color: "white",
        }}
      >
        <div style={{ fontSize: 120, fontWeight: 800, letterSpacing: -4 }}>
          Remotion works.
        </div>
        <div style={{ fontSize: 32, opacity: 0.75, marginTop: 16 }}>
          Rendered from Claude Code on the web.
        </div>
      </div>
    </AbsoluteFill>
  );
};
