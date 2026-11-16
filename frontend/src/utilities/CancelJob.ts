import axios from "axios";
import { useState } from "react";

export const cancelJob = async (id: string) => {
  try {
    const res = await axios.post(
      `http://localhost:8000/downloads/${id}/cancel`,
    );

    console.log("status", res.data);
  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.log(err.response?.data?.detail);
    }
  }
};
