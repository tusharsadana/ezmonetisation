import { createContext, useState } from "react";
import React, { ReactNode } from "react";
import { IWatchHoursState } from "../models/watch.model";
import { IVideoMap } from "../models/watch.model";

const initialWatchHoursState: IWatchHoursState = {
    videoMap: {},
    maxVideos: 10,
    blurVideo: true,
    setVideoMap: () => {},
    setMaxVideos: () => {},
    setBlurVideo: () => {}
};

export const WatchHoursContext = createContext<IWatchHoursState>(initialWatchHoursState);

export function WatchHoursProvider({ children }: { children: ReactNode }): React.ReactElement {
    const [videoMap, setVideoMap] = useState<IVideoMap>({});
    const [maxVideos, setMaxVideos] = useState<number | undefined>();
    const [blurVideo, setBlurVideo] = useState<boolean>(true);
    
    return (
        <WatchHoursContext.Provider
            value={{
                videoMap,
                maxVideos,
                blurVideo,
                setVideoMap,
                setMaxVideos,
                setBlurVideo
            }}
        >
            {children}
        </WatchHoursContext.Provider>
    );
}