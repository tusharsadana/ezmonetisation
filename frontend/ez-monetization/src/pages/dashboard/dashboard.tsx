import {
  Button,
  Card,
  Grid,
  MenuItem,
  Select,
  SelectChangeEvent,
  Typography,
} from "@mui/material";
import React, { useContext, useEffect, useState } from "react";
import CallMadeIcon from "@mui/icons-material/CallMade";
import { useNavigate } from "react-router-dom";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import {
  format,
  subWeeks,
  subDays,
  subMonths,
  subYears,
  parseISO,
} from "date-fns";
import Cookies from "universal-cookie";
import { Line } from "react-chartjs-2";
import { USER_EMAIL } from "../../contexts/auth.context";
import { axiosAPIConfig, httpGet } from "../../services/api.service";
import { IDataPoint } from "../../models/dashboard.model";
import { AxiosError } from "axios";
import { toast } from "react-toastify";
import { WatchHoursContext } from "../../contexts/watch-hours.context";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard: React.FC = () => {
  const cookie = new Cookies();
  const navigate = useNavigate();
  const [scaleWatch, setScaleWatch] = useState("day");
  const { maxVideos } = useContext(WatchHoursContext);

  //   const [scaleSub, setScaleSub] = useState("day");
  const [watchGraphData, setWatchGraphData] = useState({
    labels: [] as string[],
    datasets: [
      {
        label: "Watch hours earned",
        data: [] as number[],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  });

  //   const [subscribersGraphData, setSubscribersGraphData] = useState({
  //     labels: [] as string[],
  //     datasets: [
  //       {
  //         label: "Subscribers earned",
  //         data: [] as number[],
  //         borderColor: "rgb(255, 99, 132)",
  //         backgroundColor: "rgba(255, 99, 132, 0.5)",
  //       },
  //     ],
  //   });

  const today = new Date();

  useEffect(() => {
    let isMounted = true;

    const fetchWatchData = async () => {
      try {
        const userEmail = cookie.get(USER_EMAIL);
        const endDate = format(today, "yyyy-MM-dd");
        let startDate: string = format(subDays(today, 30), "yyyy-MM-dd");
        if (scaleWatch === "week")
          startDate = format(subWeeks(today, 12), "yyyy-MM-dd");
        else if (scaleWatch === "month")
          startDate = format(subMonths(today, 12), "yyyy-MM-dd");
        else if (scaleWatch === "year")
          startDate = format(subYears(today, 2), "yyyy-MM-dd");

        const urlWithParams = `v1/dashboard/watch-hours-earned-graph?user_email=${userEmail}&start_date=${startDate}&end_date=${endDate}&scale=${scaleWatch}`;
        const response = await httpGet<IDataPoint[]>(
          urlWithParams,
          axiosAPIConfig
        );
        return response;
      } catch (error) {
        console.error("Error fetching watch hours data.");
        return [] as IDataPoint[];
      }
    };

    const watchData = async () => {
      const graphPoints: IDataPoint[] = await fetchWatchData();

      if (isMounted) {
        let labels = graphPoints.map((item) =>
          item.x.substring(0, item.x.indexOf("T"))
        );

        if (scaleWatch === "month") {
          labels = labels.map((item) => format(parseISO(item), "MMMM, yyyy"));
        }
        const data = graphPoints.map((item) => item.y);

        setWatchGraphData({
          labels,
          datasets: [
            {
              label: "Watch hours earned",
              data: data,
              borderColor: "rgb(255, 99, 132)",
              backgroundColor: "rgba(255, 99, 132, 0.5)",
            },
          ],
        });
      }
    };

    watchData();

    return () => {
      isMounted = false;
    };
  }, [scaleWatch]);

  //   useEffect(() => {
  //     let isMounted = true;
  //     const fetchSubscribersData = async () => {
  //       try {
  //         const userEmail = cookie.get(USER_EMAIL);
  //         const time_period = scaleSub.toUpperCase();
  //         const urlWithParams = `v1/dashboard/subscribers-earned-graph?user_email=${userEmail}&time_period=${time_period}`;
  //         const response = await httpGet(urlWithParams, axiosAPIConfig);
  //         if (isMounted) {
  //           console.log(response);
  //         }
  //       } catch (error) {
  //         const axiosError = error as AxiosError;
  //         if (axiosError.response?.status == 400) {
  //           toast.error("Not data found for subscribers!");
  //         }
  //         console.error("Error fetching subscribers data.");
  //       }
  //     };
  //     fetchSubscribersData();
  //     return () => {
  //       isMounted = false;
  //     };
  //   }, [scaleSub]);

  const watchOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        // text: "Watch hours earned",
      },
    },
    elements: {
      line: {
        tension: 0.6,
      },
      point: {
        radius: 4,
        pointBorderColor: "black",
        pointBackgroundColor: "rgba(255, 99, 132, 0.8)",
        pointStyle: "circle",
        fill: false,
        borderWidth: 0.2,
      },
    },
  };

  //   const subOptions = {
  //     responsive: true,
  //     plugins: {
  //       legend: {
  //         position: "top" as const,
  //       },
  //       title: {
  //         display: true,
  //         text: "Subscribers earned",
  //       },
  //     },
  //   };

  return (
    <>
      <Typography variant="h3" component="h3" gutterBottom align="left">
        Dashboard
      </Typography>
      <Grid
        container
        spacing={2}
        display="flex"
        justifyContent="flex-start"
        sx={{
          width: "100%",
        }}
      >
        <Grid item xs={6} sm={6} md={8}>
          <Card
            variant="outlined"
            sx={{
              boxShadow: "none",
            }}
          >
            <Grid
              container
              display="flex"
              sx={{
                padding: "3%",
                alignItems: "start",
                justifyContent: "space-between",
              }}
            >
              <Grid item xs={6} sm={4} md={6}>
                <Typography variant="h5" align="left" sx={{ paddingTop: "1%" }}>
                  Watch hours earned
                </Typography>
              </Grid>
              <Grid item xs={2} sm={2} md={2}>
                <Select
                  value={scaleWatch}
                  sx={{
                    fontSize: "0.8rem",
                    flexGrow: 1,
                    textTransform: "none",
                    boxShadow: "none",
                    borderRadius: 2,
                  }}
                  defaultValue="day"
                  onChange={(event: SelectChangeEvent) => {
                    setScaleWatch(event.target.value);
                  }}
                >
                  <MenuItem value={"day"}>Day</MenuItem>
                  <MenuItem value={"week"}>Week</MenuItem>
                  <MenuItem value={"month"}>Month</MenuItem>
                  <MenuItem value={"year"}>Year</MenuItem>
                </Select>
              </Grid>
            </Grid>
            <Grid
              container
              display="flex"
              sx={{
                padding: "2%",
                marginTop: "-5%",
              }}
            >
              <Line data={watchGraphData} options={watchOptions} />
            </Grid>
          </Card>
        </Grid>
        <Grid item xs={6} sm={4} md={4}>
          <Card
            variant="outlined"
            sx={{
              boxShadow: "none",
              backgroundColor: "aquamarine",
              borderRadius: 2,
              color: "#5569ff",
              padding: "5%",
              display: "flex",
              flexDirection: "column",
              justifyItems: "center",
              gap: "10px"
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
                borderRadius: 2,
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
          </Card>
        </Grid>
        {/* <Grid item xs={12} sm={6} md={10}>
          <Paper sx={{ padding: 2, textAlign: "left", boxShadow: "none" }}>
            <Typography variant="h6" align="left">
              Subscribers earned per day
            </Typography>
            <Box display="flex" flexDirection="row" alignItems="center" gap="5px">
              <Line data={subscribersGraphData} options={subOptions} />
              <Select
                sx={{
                  maxHeight: "15%",
                }}
                value={scaleSub}
                inputProps={{ "aria-label": "Without label" }}
                defaultValue="day"
                onChange={(event: SelectChangeEvent) => {
                  setScaleSub(event.target.value);
                }}
              >
                <MenuItem value={"day"}>Day</MenuItem>
                <MenuItem value={"week"}>Week</MenuItem>
                <MenuItem value={"month"}>Month</MenuItem>
                <MenuItem value={"year"}>Year</MenuItem>
              </Select>
            </Box>
          </Paper>
        </Grid> */}
      </Grid>
    </>
  );
};

export default Dashboard;
