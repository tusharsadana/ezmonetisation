import React from "react";
import "../../App.css";
import { loadStripe } from "@stripe/stripe-js";
import { USER_EMAIL } from "../../contexts/auth.context";
import Cookies from "universal-cookie";
import { axiosAPIConfig, httpPost } from "../../services/api.service";
import { ICheckoutResponse } from "../../models/plans.model";
import { Button, Card, CardContent, Typography } from "@mui/material";

const stripePromise = loadStripe(
  process.env.PK_TEST_KEY as string
);

const Plans: React.FC = () => {
  const cookie = new Cookies();

  const redirectToCheckout = async () => {
    try {
      const stripe = await stripePromise;
      const price_id = "price_1ObcCzSEIqf7sHE3a3GHSfCs";
      const success_url = "http://localhost:5173/plans/success";
      const cancel_url = "http://localhost:5173/plans/cancel";
      const user_email = cookie.get(USER_EMAIL);
      const quantity = 1;

      const urlWithParams = `http://localhost:8000/api/v1/payment/create-checkout-session?price_id=${price_id}&success_url=${success_url}&cancel_url=${cancel_url}&user_email=${user_email}&quantity=${quantity}`;

      const response = await httpPost<ICheckoutResponse>(
        urlWithParams,
        axiosAPIConfig
      );

      if (response.sessionId) {
        const result = await stripe?.redirectToCheckout({
          sessionId: response.sessionId,
        });

        if (result?.error) {
          console.error("Stripe API Error:", result.error.message);
        }
      } else {
        console.log("Error: Missing sessionId in the response");
      }
    } catch (error) {
      console.error("Unexpected Error:", error);
    }
  };

  return (
    <Card style={{ maxWidth: 300, margin: "auto" }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Premium Plan
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Monthly Subscription
        </Typography>
        <Typography variant="h4" style={{ marginTop: 10, marginBottom: 20 }}>
          ₹100.00
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Enjoy premium features with our monthly subscription plan.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          sx={{
            borderRadius: 2,
            textTransform: "none",
            boxShadow: "none",
            textShadow: "none",
            marginTop: "5%",
            fontSize: "small",
            minWidth: "18%",
            overflow: "hidden",
          }}
          onClick={redirectToCheckout}
        >
          Subscribe Now
        </Button>
      </CardContent>
    </Card>
  );
};

export default Plans;
