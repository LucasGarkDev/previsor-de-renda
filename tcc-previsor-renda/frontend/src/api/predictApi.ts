import { PredictInput, PredictResponse } from "../types/Predict";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
const PREDICT_ENDPOINT = buildApiUrl(API_URL, "/predict");

type ApiErrorPayload = {
  detail?: string;
};

function buildApiUrl(baseUrl: string, path: string): string {
  if (!baseUrl || baseUrl === "/") {
    return path;
  }

  return `${baseUrl.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`;
}

export async function predictRenda(
  data: PredictInput
): Promise<PredictResponse> {
  const response = await fetch(PREDICT_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    let message = "Erro ao consultar a API de predicao";

    try {
      const payload = (await response.json()) as ApiErrorPayload;
      if (payload.detail) {
        message = payload.detail;
      }
    } catch {
      // Ignore invalid error bodies and keep the default message.
    }

    throw new Error(message);
  }

  return response.json();
}
