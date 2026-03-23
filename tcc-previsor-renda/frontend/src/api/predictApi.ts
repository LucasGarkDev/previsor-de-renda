import { PredictInput, PredictResponse } from "../types/Predict";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export async function predictRenda(
  data: PredictInput
): Promise<PredictResponse> {
  const response = await fetch(API_URL + "/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Erro ao consultar a API de predicao");
  }

  return response.json();
}
