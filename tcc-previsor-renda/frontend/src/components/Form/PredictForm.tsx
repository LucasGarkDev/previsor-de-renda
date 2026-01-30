// frontend/src/components/Form/PredictForm.tsx
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
    } catch (err) {
      setError("Erro ao consultar o modelo. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Informe seus dados</h2>

      <DemografiaSection data={formData} setData={setFormData} />
      <TrabalhoSection data={formData} setData={setFormData} />
      <LocalizacaoSection data={formData} setData={setFormData} />
      <DomicilioSection data={formData} setData={setFormData} />

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? "Calculando..." : "Prever renda"}
      </button>
    </form>
  );
}
