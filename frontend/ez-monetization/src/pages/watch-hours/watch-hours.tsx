import WatchHoursDescription from "./components/watch-hours.description";
import WatchHoursSlider from "./components/watch-hours.slider";
import WatchHoursPanel from "./components/watch-hours.panel";

export default function WatchHours(): JSX.Element {
  return (
    <>
      <WatchHoursDescription />
      <WatchHoursSlider />
      <WatchHoursPanel />
    </>
  );
}
