// frontend/src/components/Result/PredictionResult.tsx
import { PredictResponse } from "../../types/Predict";
import "./PredictionResult.css";

interface Props {
  result: PredictResponse;
  onReset: () => void;
}

export default function PredictionResult({ result, onReset }: Props) {
  return (
    <div className="result-box">
      <h2>Resultado da estimativa</h2>

      <div className="result-main">
        R$ {result.renda_estimada.toFixed(2)}
      </div>

      <div className="result-interval">
        Intervalo provável: <br />
        <strong>
          R$ {result.intervalo_provavel.min.toFixed(2)} —{" "}
          R$ {result.intervalo_provavel.max.toFixed(2)}
        </strong>
      </div>

      <div className="result-error">
        Erro médio do modelo: ± R$ {result.erro_medio_modelo.toFixed(2)}
      </div>

      <p className="result-note">{result.observacao}</p>

      <button onClick={onReset}>Nova simulação</button>
    </div>
  );
}
