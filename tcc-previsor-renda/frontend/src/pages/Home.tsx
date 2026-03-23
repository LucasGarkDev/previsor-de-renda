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
            <span className="hero-tag">Predicao orientada por dados</span>
            <h2>Simule a renda estimada com uma interface mais clara e objetiva.</h2>
            <p>
              Informe dados demograficos, trabalho, localizacao e domicilio para
              gerar uma estimativa com intervalo provavel e leitura imediata do
              resultado.
            </p>
          </div>

          <div className="hero-metrics">
            <article>
              <strong>4 blocos</strong>
              <span>Formulario organizado em secoes</span>
            </article>
            <article>
              <strong>Leitura rapida</strong>
              <span>Resultado destacado com contexto</span>
            </article>
            <article>
              <strong>Responsivo</strong>
              <span>Fluxo adaptado para desktop e mobile</span>
            </article>
          </div>
        </section>

        <section className="content-grid">
          <aside className="insight-card">
            <span className="insight-eyebrow">Como funciona</span>
            <h3>O modelo combina variaveis socioeconomicas para estimar renda.</h3>
            <p>
              A interface foi reorganizada para reduzir ruido visual, destacar
              decisoes importantes e deixar a simulacao mais natural em telas
              menores.
            </p>

            <ul className="insight-list">
              <li>Campos agrupados por contexto real de preenchimento.</li>
              <li>Hierarquia visual focada em leitura e contraste.</li>
              <li>Resposta final com valor central, faixa provavel e observacao.</li>
            </ul>
          </aside>

          <div className="card">
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
