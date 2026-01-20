from backend.app.schemas.predict import PredictInput
from backend.app.core.feature_builder import build_model_features


def main():
    # Payload de teste (conceitual, como viria do frontend)
    payload = PredictInput(
        idade=35,
        anos_estudo=11,
        ultimo_grau_frequentado="medio_completo",
        sabe_ler_escrever=True,
        sexo="masculino",
        raca_cor="parda",

        trabalhou_semana=True,
        horas_trabalhadas_semana=40,
        ocupacao_semana=True,
        atividade_ramo_negocio_semana=17,
        posicao_ocupacao="empregado",
        possui_carteira_assinada=True,

        sigla_uf="ES",
        zona_urbana=True,
        regiao_metropolitana=False,

        total_pessoas=4,
        quantidade_comodos=5,
        quantidade_dormitorios=2,

        possui_agua_rede=True,
        tipo_esgoto="rede",
        lixo_coletado=True,
        possui_iluminacao_eletrica=True,

        possui_geladeira=True,
        possui_tv=True,
        possui_fogao=True,
        possui_radio=False,
    )

    # Construir features do modelo
    df = build_model_features(payload)

    print("\n=== DataFrame gerado ===")
    print(df)

    print("\n=== Colunas ===")
    print(df.columns.tolist())

    print("\n=== Tipos ===")
    print(df.dtypes)


if __name__ == "__main__":
    main()
