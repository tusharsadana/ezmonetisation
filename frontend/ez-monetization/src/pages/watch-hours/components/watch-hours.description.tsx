import { Chip, Box, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CallMadeIcon from "@mui/icons-material/CallMade";
import { IUserPrivileges } from "../../../models/watch.model";
import { useState, useEffect, useContext } from "react";
import { httpGet } from "../../../services/api.service";
import Cookies from "universal-cookie";
import { USER_EMAIL } from "../../../contexts/auth.context";
import { axiosAPIConfig } from "../../../services/api.service";
import { WatchHoursContext } from "../../../contexts/watch-hours.context";

const WatchHoursDescription: React.FC = () => {
  const navigate = useNavigate();
  const cookie = new Cookies();
  const [userPrivileges, setUserPrivileges] = useState<IUserPrivileges>();
  const { setMaxVideos, maxVideos } = useContext(WatchHoursContext);

  useEffect(() => {
    const setPrivilegeValues = async () => {
      try {
        const userEmail = cookie.get(USER_EMAIL);
        const urlWithParams = `/v1/video/user-watch-hours-privileges?user_email=${userEmail}`;
        const response = await httpGet<IUserPrivileges>(
          urlWithParams,
          axiosAPIConfig
        );
        setUserPrivileges(response);
        console.log(userPrivileges);
      } catch (error) {
        console.error("Error fetching user privileges:", error);
      }
    };

    setPrivilegeValues();
  }, []);

  setMaxVideos(userPrivileges?.maximum_videos_allowed === undefined ? 10 : userPrivileges?.maximum_videos_allowed);
  const eachVideoTime = userPrivileges?.maximum_video_duration || 0;
  const ratio = userPrivileges?.watch_hours_ratio || 0;
  const userType = userPrivileges?.user_type || "Free User";
  const watchHoursFor10Videos = (10 * eachVideoTime * ratio) / 60;

  return (
    <>
      <Typography variant="h3" component="h3" gutterBottom align="left">
        Earn Watch Hours
      </Typography>
      <Typography variant="h6" component="h6" gutterBottom align="left">
        You are{" "}
        <Chip
          label={userType}
          color="primary"
          sx={{
            backgroundColor: userType === "Free User" ? "#6E759F" : "#5569ff",
          }}
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
          paddingLeft: "2%",
          color: "#5569ff",
        }}
      >
        <Typography variant="h6" component="h6" gutterBottom align="left">
          You can watch up to {maxVideos} Videos at a time. To increase your
          limit, please upgrade your plan.{" "}
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
            marginLeft: "5%",
            textShadow: "none",
            fontSize: "small",
            minWidth: "18%",
            textOverflow: "ellipsis",
            overflow: "hidden",
          }}
          endIcon={<CallMadeIcon />}
        >
          Upgrade Now
        </Button>
      </Box>
    </>
  );
};

export default WatchHoursDescription;
