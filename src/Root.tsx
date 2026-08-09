import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { RhodyStrollsLogo } from "./animations/RhodyStrollsLogo";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={90}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="RhodyStrolls"
        component={RhodyStrollsLogo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
