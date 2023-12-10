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
import { useEffect } from "react";
import { axiosAPI, axiosAPIConfig, httpGet } from "../../services/api.service";
import Cookies from "universal-cookie";
import { USER_EMAIL } from "../../contexts/auth.context";

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
  const videos_link = signal("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userEmail = cookie.get(USER_EMAIL);
        const numberOfVideos = 10;
        const urlWithParams = `/video/fetch-videos?user_email=${userEmail}&number_of_videos=${numberOfVideos}`;
        const data = await httpGet<string>(urlWithParams, axiosAPIConfig);

        videos_link.value = data;
      } catch (error) {
        console.error("Error fetching video data:", error);
      }
    };

    fetchData();
  }, [videos_link.value]);

  const navigate = useNavigate();

  const sliderValue = signal(1);

  const user = "GOLD"; // fetch using backend
  const selectedUser = userType.find((u) => u.user === user);

  const maxVideos = selectedUser?.numVideos || 0;
  const marks = [];

  for (let value = 1; value <= maxVideos; value++) {
    if (value % 5 == 0) {
      marks.push({ value, label: `${value}` });
    } else {
      marks.push({ value });
    }
  }

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    sliderValue.value = newValue as number;
  };

  const eachVideoTime = selectedUser?.eachVideoTime || 0;
  const ratio = selectedUser?.ratio || 0;

  const watchHoursFor10Videos = (10 * eachVideoTime * ratio) / 60;

  return (
    <>
      <Typography variant="h3" component="h3" gutterBottom align="left">
        Earn Watch hours
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
            value={sliderValue.value}
            valueLabelDisplay="off"
            step={null}
            onChange={handleSliderChange}
            max={100}
            marks={marks}
            sx={{
              width: "50%",
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
            sx={{ padding: "10px" }}
          >
            Videos: {sliderValue.value}
          </Typography>
          <Button
            color="primary"
            variant="contained"
            size="medium"
            onClick={() => {
              // fetch videos call
            }}
            sx={{
              borderRadius: 20,
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
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((item) => (
          <Grid item xs={12} sm={6} md={3} key={item}>
            <Paper elevation={0} sx={{ padding: 2, textAlign: "left" }}>
              <Typography variant="h6" align="left">
                Video {item}
              </Typography>
              <Typography align="left">Shadowed clip {item}.</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </>
  );
}
