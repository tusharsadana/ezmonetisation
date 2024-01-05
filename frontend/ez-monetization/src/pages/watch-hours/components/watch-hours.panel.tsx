import {
  Grid,
  Paper,
  Typography,
  FormGroup,
  FormControlLabel,
  Switch,
  Box,
} from "@mui/material";
import { useContext } from "react";
import { httpPost } from "../../../services/api.service";
import Cookies from "universal-cookie";
import { USER_EMAIL } from "../../../contexts/auth.context";
import { axiosAPIConfig } from "../../../services/api.service";
import { toast } from "react-toastify";
import YouTube, { YouTubeProps } from "react-youtube";

import { WatchHoursContext } from "../../../contexts/watch-hours.context";

const WatchHoursPanel: React.FC = () => {
  const cookie = new Cookies();

  const { videoMap, blurVideo } = useContext(WatchHoursContext);

  const videoTimes = Array(100).fill(null);
  const setIntervalForMinutes = async (videoIndex: number, videoId: string) => {
    const tempInterval = setInterval(async () => {
      await videoCompleted(videoIndex, videoId);
    }, 6 * 1000 * 60);
    updateVideoTime(videoIndex, tempInterval);
  };

  const updateVideoTime = (videoIndex: number, interval: any) => {
    videoTimes[videoIndex] = interval;
  };

  const videoCompleted = async (videoIndex: number, videoId: string) => {
    const durationRan = 6 / 60;

    try {
      const response = await httpPost<any>(
        "/v1/video/video_completion",
        {
          user_email: cookie.get(USER_EMAIL),
          video_id: videoId,
          video_duration: durationRan,
        },
        axiosAPIConfig
      );
      clearInterval(videoTimes[videoIndex]);
      console.log(response.data);
      toast.success("Video " + (videoIndex + 1) + " completed successfully.");
      updateVideoTime(videoIndex, 0);
    } catch (error) {
      console.error("Error completing video:", error);
    }
  };

  const opts: YouTubeProps["opts"] = {
    height: "200",
    width: "100%",
    playerVars: {
      autoplay: 1,
      mute: 1,
      fs: 0,
    },
  };

  return (
    <>
      <Box
        sx={{
          paddingLeft: "20px",
        }}
      >
        <Grid container spacing={2} justifyContent="flex-start">
          {Object.entries(videoMap).map(([videoId, { video_link, index }]) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Paper elevation={0} sx={{ padding: 2, textAlign: "left" }}>
                <Typography variant="h6" align="left">
                  Video {index + 1}
                </Typography>
                <div
                  style={{
                    position: "relative",
                    filter: blurVideo ? "blur(1.2px)" : "none",
                  }}
                >
                  <YouTube
                    videoId={video_link}
                    opts={opts}
                    onEnd={() => videoCompleted(index, videoId)}
                    onPlay={() => {
                      setIntervalForMinutes(index, videoId);
                    }}
                  />
                </div>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>
    </>
  );
};

export default WatchHoursPanel;
