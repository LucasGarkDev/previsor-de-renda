import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function TrabalhoSection({ data, setData }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Trabalho</legend>
      <p className="section-description">
        Informacoes sobre ocupacao, jornada e vinculo profissional.
      </p>

      <div className="fieldset-grid">
        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.trabalhou_semana}
            onChange={(e) => setData({ ...data, trabalhou_semana: e.target.checked })}
          />
          <span>Trabalhou na ultima semana</span>
        </label>

        <label className="field">
          <span>Horas trabalhadas por semana</span>
          <input
            type="number"
            min={0}
            value={data.horas_trabalhadas_semana}
            onChange={(e) =>
              setData({
                ...data,
                horas_trabalhadas_semana: Number(e.target.value),
              })
            }
          />
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.ocupacao_semana}
            onChange={(e) => setData({ ...data, ocupacao_semana: e.target.checked })}
          />
          <span>Esta ocupado atualmente</span>
        </label>

        <label className="field">
          <span>Ramo de atividade (codigo PNAD)</span>
          <input
            type="number"
            min={0}
            value={data.atividade_ramo_negocio_semana}
            onChange={(e) =>
              setData({
                ...data,
                atividade_ramo_negocio_semana: Number(e.target.value),
              })
            }
          />
        </label>

        <label className="field">
          <span>Posicao na ocupacao</span>
          <select
            value={data.posicao_ocupacao}
            onChange={(e) =>
              setData({
                ...data,
                posicao_ocupacao: e.target.value as any,
              })
            }
          >
            <option value="empregado">Empregado</option>
            <option value="empregador">Empregador</option>
            <option value="conta_propria">Conta propria</option>
            <option value="outro">Outro</option>
          </select>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_carteira_assinada}
            onChange={(e) =>
              setData({
                ...data,
                possui_carteira_assinada: e.target.checked,
              })
            }
          />
          <span>Possui carteira assinada</span>
        </label>
      </div>
    </fieldset>
  );
}
