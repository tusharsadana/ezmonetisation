export interface IVideo {
  video_id: string;
  video_link: string;
}

export interface IVideoMap {
  [video_id: string]: {
    video_link: string;
    index: number;
  };
}
