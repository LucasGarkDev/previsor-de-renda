import { PredictResponse } from "../../types/Predict";
import "./PredictionResult.css";

interface Props {
  result: PredictResponse;
  onReset: () => void;
}

export default function PredictionResult({ result, onReset }: Props) {
  const renda = result.renda_estimada.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  const minimo = result.intervalo_provavel.min.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  const maximo = result.intervalo_provavel.max.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
  const erro = result.erro_medio_modelo.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });

  return (
    <div className="result-box">
      <span className="result-eyebrow">Estimativa concluida</span>
      <h2>Resultado da simulacao</h2>

      <div className="result-main">{renda}</div>

      <div className="result-summary-grid">
        <article className="result-panel result-panel-primary">
          <span>Faixa provavel</span>
          <strong>
            {minimo} ate {maximo}
          </strong>
        </article>

        <article className="result-panel">
          <span>Erro medio do modelo</span>
          <strong>+- {erro}</strong>
        </article>
      </div>

      <p className="result-note">{result.observacao}</p>

      <button onClick={onReset}>Nova simulacao</button>
    </div>
  );
}
