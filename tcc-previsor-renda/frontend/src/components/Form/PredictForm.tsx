import "./Form.css";

import { useState } from "react";
import { PredictInput, PredictResponse } from "../../types/Predict";
import { predictRenda } from "../../api/predictApi";

import DemografiaSection from "./DemografiaSection";
import TrabalhoSection from "./TrabalhoSection";
import LocalizacaoSection from "./LocalizacaoSection";
import DomicilioSection from "./DomicilioSection";

interface Props {
  onResult: (result: PredictResponse) => void;
}

export default function PredictForm({ onResult }: Props) {
  const [formData, setFormData] = useState<PredictInput>({
    idade: 30,
    anos_estudo: 11,
    ultimo_grau_frequentado: "medio_completo",
    sabe_ler_escrever: true,
    sexo: "masculino",
    raca_cor: "parda",

    trabalhou_semana: true,
    horas_trabalhadas_semana: 40,
    ocupacao_semana: true,
    atividade_ramo_negocio_semana: 17,
    posicao_ocupacao: "empregado",
    possui_carteira_assinada: true,

    sigla_uf: "ES",
    zona_urbana: true,
    regiao_metropolitana: false,

    total_pessoas: 4,
    quantidade_comodos: 5,
    quantidade_dormitorios: 2,

    possui_agua_rede: true,
    tipo_esgoto: "rede",
    lixo_coletado: true,
    possui_iluminacao_eletrica: true,

    possui_geladeira: true,
    possui_tv: true,
    possui_fogao: true,
    possui_radio: false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await predictRenda(formData);
      onResult(response);
    } catch {
      setError("Erro ao consultar o modelo. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="predict-form" onSubmit={handleSubmit}>
      <div className="form-intro">
        <div>
          <span className="form-eyebrow">Simulacao</span>
          <h2>Informe os dados para gerar a estimativa.</h2>
          <p>
            O preenchimento foi distribuido em secoes para facilitar a leitura e
            reduzir erro no envio.
          </p>
        </div>

        <div className="form-status-card">
          <span>Etapas</span>
          <strong>4 blocos de entrada</strong>
          <small>Demografia, trabalho, localizacao e domicilio.</small>
        </div>
      </div>

      <DemografiaSection data={formData} setData={setFormData} />
      <TrabalhoSection data={formData} setData={setFormData} />
      <LocalizacaoSection data={formData} setData={setFormData} />
      <DomicilioSection data={formData} setData={setFormData} />

      {error && <p className="form-error">{error}</p>}

      <div className="form-actions">
        <p className="form-helper">
          Revise os campos principais antes de enviar. O resultado exibira uma
          faixa provavel, nao apenas um valor unico.
        </p>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? "Calculando estimativa..." : "Prever renda"}
        </button>
      </div>
    </form>
  );
}
