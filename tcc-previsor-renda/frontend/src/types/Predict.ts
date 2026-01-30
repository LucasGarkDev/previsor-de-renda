// frontend/src/types/Predict.ts
// ===== INPUT =====
export interface PredictInput {
  // Demografia
  idade: number;
  anos_estudo: number;
  ultimo_grau_frequentado:
    | "fundamental_incompleto"
    | "fundamental_completo"
    | "medio_incompleto"
    | "medio_completo"
    | "superior_incompleto"
    | "superior_completo";

  sabe_ler_escrever: boolean;
  sexo: "masculino" | "feminino";
  raca_cor: "branca" | "preta" | "parda" | "amarela" | "indigena";

  // Trabalho
  trabalhou_semana: boolean;
  horas_trabalhadas_semana: number;
  ocupacao_semana: boolean;
  atividade_ramo_negocio_semana: number;
  posicao_ocupacao: "empregado" | "empregador" | "conta_propria" | "outro";
  possui_carteira_assinada: boolean;

  // Localização
  sigla_uf: string;
  zona_urbana: boolean;
  regiao_metropolitana: boolean;

  // Domicílio
  total_pessoas: number;
  quantidade_comodos: number;
  quantidade_dormitorios: number;

  possui_agua_rede: boolean;
  tipo_esgoto: "rede" | "fossa" | "outro" | "nao_informado";
  lixo_coletado: boolean;
  possui_iluminacao_eletrica: boolean;

  possui_geladeira: boolean;
  possui_tv: boolean;
  possui_fogao: boolean;
  possui_radio: boolean;
}

// ===== OUTPUT =====
export interface PredictResponse {
  renda_estimada: number;
  intervalo_provavel: {
    min: number;
    max: number;
  };
  erro_medio_modelo: number;
  observacao: string;
}
