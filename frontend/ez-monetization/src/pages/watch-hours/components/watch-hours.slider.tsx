import { Grid, Slider, Box, Typography, Button, FormGroup, FormControlLabel, Switch } from "@mui/material";
import { CallReceived } from "@mui/icons-material";
import { useState, useContext } from "react";
import { httpGet } from "../../../services/api.service";
import Cookies from "universal-cookie";
import { USER_EMAIL } from "../../../contexts/auth.context";
import { IVideo, IVideoMap } from "../../../models/watch.model";
import { axiosAPIConfig } from "../../../services/api.service";
import { WatchHoursContext } from "../../../contexts/watch-hours.context";

const WatchHoursSlider: React.FC = () => {
  const { setVideoMap, maxVideos, setBlurVideo, blurVideo } =
    useContext(WatchHoursContext);
  const cookie = new Cookies();

  const fetchData = async () => {
    try {
      const userEmail = cookie.get(USER_EMAIL);
      const numberOfVideos = 1;
      const urlWithParams = `/v1/video/fetch-videos?user_email=${userEmail}&number_of_videos=${numberOfVideos}`;
      const response = await httpGet<IVideo[]>(urlWithParams, axiosAPIConfig);

      setVideoMap(
        response.reduce((acc, { video_id, video_link }, index) => {
          acc[video_id] = { video_link, index };
          return acc;
        }, {} as IVideoMap)
      );
    } catch (error) {
      console.error("Error fetching video data:", error);
    }
  };

  const [sliderValue, setSliderValue] = useState(1);
  const marks = [];

  for (
    let value = 1;
    value <= (maxVideos === undefined ? 10 : maxVideos);
    value++
  ) {
    if (value % (maxVideos === undefined ? 10 : maxVideos) == 0 || value == 1) {
      marks.push({ value, label: `${value}` });
    } else {
      marks.push({ value });
    }
  }

  const handleOnChangeSlider = (event: Event, newValue: number | number[]) => {
    setSliderValue(newValue as number);
  };
  return (
    <>
      <Box
        sx={{
          padding: 4,
          borderRadius: 5,
          marginTop: 2,
          paddingLeft: "20px",
        }}
      >
        <Grid container gap="9px" sx={{ display: "flex", alignItems: "center" }}>
          <Grid item xs={7}>
            <Typography variant="h6" component="h6" gutterBottom align="left">
              How many videos do you want to watch at a time?
            </Typography>
          </Grid>
          <Grid item xs={2}>
            <Typography
              variant="h6"
              component="h6"
              color="primary"
              sx={{ padding: "7px" }}
            >
              Videos: {sliderValue}
            </Typography>
          </Grid>
          <Grid item xs={2}>
            <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  defaultChecked
                  onChange={() => {
                    setBlurVideo(!blurVideo);
                  }}
                />
              }
              label="Blur"
            />
          </FormGroup>
          </Grid>
        </Grid>
        <Grid
          container
          sx={{ display: "flex", gap: "20px", justifyContent: "space-between" }}
        >
          <Grid item xs={6}>
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
                flexGrow: 2,
                padding: "15px",
                marginTop: "5px",
                display: "flex",
                justifyContent: "flex-start",
              }}
            />
          </Grid>
          <Grid item xs={3}>
            <Button
              color="primary"
              variant="contained"
              size="medium"
              onClick={() => {
                fetchData();
              }}
              sx={{
                borderRadius: 2,
                flexGrow: 1,
                textTransform: "none",
                fontSize: "0.9rem",
                boxShadow: "none",
                textShadow: "none",
                marginBottom: "15px",
                marginTop: "5px",
                padding: "10px 10px",
              }}
              startIcon={<CallReceived />}
            >
              Fetch Videos
            </Button>
          </Grid>
        </Grid>
      </Box>
    </>
  );
};

export default WatchHoursSlider;
