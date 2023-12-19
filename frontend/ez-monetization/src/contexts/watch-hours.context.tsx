import { createContext, useState } from "react";
import React, { ReactNode } from "react";
import { IWatchHoursState } from "../models/watch.model";
import { IVideoMap } from "../models/watch.model";

const initialWatchHoursState: IWatchHoursState = {
    videoMap: {},
    maxVideos: 10,
    setVideoMap: () => {},
    setMaxVideos: () => {},
};

export const WatchHoursContext = createContext<IWatchHoursState>(initialWatchHoursState);

export function AuthProvider({ children }: { children: ReactNode }): React.ReactElement {
    const [videoMap, setVideoMap] = useState<IVideoMap>({});
    const [maxVideos, setMaxVideos] = useState<number | undefined>();
    
    return (
        <WatchHoursContext.Provider
            value={{
                videoMap,
                maxVideos,
                setVideoMap,
                setMaxVideos
            }}
        >
            {children}
        </WatchHoursContext.Provider>
    );
}