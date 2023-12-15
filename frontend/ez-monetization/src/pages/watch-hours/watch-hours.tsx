import {
  Typography,
  Chip,
  Box,
  Slider,
  Grid,
  Paper,
  Button,
} from "@mui/material";
import CallMadeIcon from "@mui/icons-material/CallMade";
import { signal } from "@preact/signals-react";
import { useNavigate } from "react-router-dom";
import { CallReceived } from "@mui/icons-material";
import { useEffect, useState } from "react";
import {
  axiosAPI,
  axiosAPIConfig,
  httpGet,
  httpPost,
} from "../../services/api.service";
import Cookies from "universal-cookie";
import { USER_EMAIL } from "../../contexts/auth.context";
import { IVideo, IVideoMap } from "../../models/watch.model";
import YouTube, { YouTubeProps } from "react-youtube";
import { toast } from "react-toastify";

export default function WatchHours(): JSX.Element {
  const userType = [
    {
      user: "IRON",
      color: "#61666A",
      eachVideoTime: 6,
      ratio: 0.1,
      numVideos: 1,
    },
    {
      user: "BRONZE",
      color: "#CD7F32",
      eachVideoTime: 6,
      ratio: 0.5,
      numVideos: 10,
    },
    {
      user: "SILVER",
      color: "#C0C0C0",
      eachVideoTime: 6,
      ratio: 1,
      numVideos: 20,
    },
    {
      user: "GOLD",
      color: "#FFD700",
      eachVideoTime: 6,
      ratio: 2,
      numVideos: 50,
    },
    {
      user: "PLATINUM",
      color: "#800080",
      eachVideoTime: 6,
      ratio: 100,
      numVideos: 100,
    },
  ];

  const cookie = new Cookies();
  const [videoMap, setVideoMap] = useState<IVideoMap>({});

  const fetchData = async () => {
    try {
      const userEmail = cookie.get(USER_EMAIL);
      const numberOfVideos = 1;
      const urlWithParams = `/v1/video/fetch-videos?user_email=${userEmail}&number_of_videos=${numberOfVideos}`;
      const data = await httpGet<IVideo[]>(urlWithParams, axiosAPIConfig);

      setVideoMap(
        data.reduce((acc, { video_id, video_link }, index) => {
          acc[video_id] = { video_link, index };
          return acc;
        }, {} as IVideoMap)
      );
    } catch (error) {
      console.error("Error fetching video data:", error);
    }
  };

  const videoTimes = Array(100).fill(null);
  const setIntervalForMinutes = async (videoIndex: number) => {
    const tempInterval = setInterval(async () => {
      await videoCompleted(videoIndex);
    }, 6 * 1000 * 60);
    updateVideoTime(videoIndex, tempInterval);

  };

  const updateVideoTime = (videoIndex: number, interval: any) => {
    videoTimes[videoIndex] = interval;
  };

  const videoCompleted = async (videoIndex: number) => {
    const videoId = Object.keys(videoMap)[videoIndex];
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
      toast.success("Video " + (videoIndex + 1) + "completed successfully.");
      // show watch hours earned
      updateVideoTime(videoIndex, 0);
    } catch (error) {
      console.error("Error completing video:", error);
    }
  };

  const navigate = useNavigate();

  const [sliderValue, setSliderValue] = useState(1);

  const user = "GOLD"; // fetch using backend
  const selectedUser = userType.find((u) => u.user === user);

  const maxVideos = selectedUser?.numVideos || 10;
  const marks = [];

  for (let value = 1; value <= maxVideos; value++) {
    if (value % maxVideos == 0 || value == 1) {
      marks.push({ value, label: `${value}` });
    } else {
      marks.push({ value });
    }
  }

  const handleOnChangeSlider = (event: Event, newValue: number | number[]) => {
    setSliderValue(newValue as number);
  };
  const eachVideoTime = selectedUser?.eachVideoTime || 0;
  const ratio = selectedUser?.ratio || 0;

  const watchHoursFor10Videos = (10 * eachVideoTime * ratio) / 60;

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
      <Typography variant="h3" component="h3" gutterBottom align="left">
        Earn Watch Hours
      </Typography>
      <Typography variant="h6" component="h6" gutterBottom align="left">
        You are{" "}
        <Chip
          label={selectedUser?.user}
          color="primary"
          sx={{ backgroundColor: selectedUser?.color }}
        />{" "}
        Member. You will have to watch these videos. Every video will run for{" "}
        {eachVideoTime} Minutes. For every 10 videos you watch for{" "}
        {eachVideoTime} Minutes, you will get {watchHoursFor10Videos.toFixed(2)}{" "}
        watch hours. If you watch 100 videos you will get{" "}
        {(100 * eachVideoTime * ratio) / 60} watch hours.
      </Typography>
      <Box
        display="flex"
        alignItems="center"
        sx={{
          backgroundColor: "aquamarine",
          padding: 2,
          borderRadius: 5,
          marginTop: 2,
          fontWeight: "bold",
          paddingLeft: "20px",
          color: "#5569ff",
        }}
      >
        <Typography variant="h6" component="h6" gutterBottom align="left">
          You can watch up to {selectedUser?.numVideos} Videos at a time. To
          increase your limit, please upgrade your plan.{" "}
        </Typography>
        <Button
          color="primary"
          variant="contained"
          size="medium"
          onClick={() => {
            navigate("/plans");
          }}
          sx={{
            borderRadius: 20,
            textTransform: "none",
            boxShadow: "none",
            marginLeft: "10px",
            marginBottom: "5px",
            textShadow: "none",
            "&:hover": {},
          }}
          endIcon={<CallMadeIcon />}
        >
          Upgrade Now
        </Button>
      </Box>

      <Box
        sx={{
          padding: 4,
          borderRadius: 5,
          marginTop: 2,
          paddingLeft: "20px",
        }}
      >
        <Typography variant="h6" component="h6" gutterBottom align="left">
          How many videos you want to watch at a time?
        </Typography>
        <Grid container sx={{ display: "flex", gap: "50px" }}>
          {/* not changing values, need to check */}
          <Slider
            aria-label="Restricted values"
            defaultValue={1}
            value={sliderValue}
            valueLabelDisplay="auto"
            step={null}
            onChange={handleOnChangeSlider}
            max={100}
            marks={marks}
            sx={{
              flexGrow: 1,
              padding: "15px",
              marginTop: "5px",
              display: "flex",
              justifyContent: "flex-start",
            }}
          />
          <Typography
            variant="h6"
            component="h6"
            color="primary"
            sx={{ padding: "10px", flexGrow: 1 }}
          >
            Videos: {sliderValue}
          </Typography>
          <Button
            color="primary"
            variant="contained"
            size="medium"
            onClick={() => {
              fetchData();
            }}
            sx={{
              borderRadius: 20,
              flexGrow: 1,
              textTransform: "none",
              fontSize: "0.9rem",
              boxShadow: "none",
              textShadow: "none",
              marginBottom: "15px",
              marginTop: "5px",
              "&:hover": {},
              padding: "10px 10px",
            }}
            startIcon={<CallReceived />}
          >
            Fetch Videos
          </Button>
        </Grid>
      </Box>
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
                  // filter: "blur(2px)",
                }}
              >
                <YouTube
                  videoId={video_link}
                  opts={opts}
                  onEnd={() => videoCompleted(index)}
                  onPlay={() => { setIntervalForMinutes(index) }
                  }
                />
              </div>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </>
  );
}
