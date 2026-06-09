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
        <section className="hero-panel">
          <div className="hero-copy">
            <span className="hero-tag">Previsor de renda</span>
            <h2>Estimativa mensal com leitura objetiva dos dados.</h2>
            <p>
              Preencha os blocos de perfil, trabalho, localizacao e domicilio.
              O sistema retorna valor estimado, faixa provavel e erro medio do
              modelo.
            </p>
          </div>

          <div className="hero-metrics">
            <article>
              <span>Modelo</span>
              <strong>Mincer + CatBoost</strong>
            </article>
            <article>
              <span>Saida</span>
              <strong>Renda + intervalo</strong>
            </article>
            <article>
              <span>Base</span>
              <strong>Variaveis PNAD</strong>
            </article>
          </div>
        </section>

        <section className="content-grid">
          <aside className="insight-card">
            <span className="insight-eyebrow">Fluxo</span>
            <h3>Entrada estruturada para reduzir erro de preenchimento.</h3>
            <p>
              Cada bloco agrupa campos que pertencem ao mesmo contexto da
              pesquisa. A previsao aparece em uma tela separada para facilitar
              a leitura do resultado.
            </p>

            <ul className="insight-list">
              <li>Conferir dados demograficos e escolaridade.</li>
              <li>Informar jornada, ocupacao e vinculo de trabalho.</li>
              <li>Completar localizacao, domicilio e bens disponiveis.</li>
              <li>Enviar para obter estimativa, faixa e observacao.</li>
            </ul>
          </aside>

          <div className="card work-card">
            {!result ? (
              <PredictForm onResult={setResult} />
            ) : (
              <PredictionResult result={result} onReset={() => setResult(null)} />
            )}
          </div>
        </section>
      </main>
    </>
  );
}
