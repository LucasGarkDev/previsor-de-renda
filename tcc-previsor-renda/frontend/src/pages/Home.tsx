// frontend/src/pages/Home.tsx
import { useState } from "react";
import Header from "../components/Header";
import PredictForm from "../components/Form/PredictForm";
import PredictionResult from "../components/Result/PredictionResult";
import { PredictResponse } from "../types/Predict";

import "./Home.css";

export default function Home() {
  const [result, setResult] = useState<PredictResponse | null>(null);

  return (
    <>
      <Header />

      <main className="home-container">
        <div className="card">
          {!result ? (
            <PredictForm onResult={setResult} />
          ) : (
            <PredictionResult
              result={result}
              onReset={() => setResult(null)}
            />
          )}
        </div>
      </main>
    </>
  );
}
