from backend.app.schemas.predict import PredictInput
from backend.app.services.predict_service import PredictService


def main():
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

    renda_estimada = PredictService.predict(payload)

    print("\n=== Renda estimada ===")
    print(f"R$ {renda_estimada:,.2f}")


if __name__ == "__main__":
    main()
