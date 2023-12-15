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

export interface IUserPrivileges {
  user_type: string;
  maximum_video_duration: number;
  watch_hours_ratio: number;
  allowed_fetch_videos: number;
  minimum_videos_allowed: number;
  maximum_videos_allowed: number;
}
