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
          <span className="switch-copy">
            <span className="switch-label">Trabalhou na ultima semana</span>
            <small>Considere qualquer trabalho remunerado no periodo.</small>
          </span>
        </label>

        <label className="field">
          <span className="field-label">Horas trabalhadas por semana</span>
          <small className="field-hint">Informe a jornada semanal habitual.</small>
          <input
            type="number"
            min={0}
            max={100}
            placeholder="Ex: 40"
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
          <span className="switch-copy">
            <span className="switch-label">Esta ocupado atualmente</span>
            <small>Marque se possui ocupacao na semana de referencia.</small>
          </span>
        </label>

        <label className="field">
          <span className="field-label">Ramo de atividade (codigo PNAD)</span>
          <small className="field-hint">Use o codigo do setor entre 11 e 25.</small>
          <input
            type="number"
            min={11}
            max={25}
            placeholder="Ex: 17"
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
          <span className="field-label">Posicao na ocupacao</span>
          <small className="field-hint">Tipo de vinculo da pessoa no trabalho.</small>
          <select
            value={data.posicao_ocupacao}
            onChange={(e) =>
              setData({
                ...data,
                posicao_ocupacao: e.target.value as any,
              })
            }
          >
            <optgroup label="Vinculo principal">
              <option value="empregado">Empregado</option>
              <option value="empregador">Empregador</option>
              <option value="conta_propria">Conta propria</option>
              <option value="outro">Outro</option>
            </optgroup>
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
          <span className="switch-copy">
            <span className="switch-label">Possui carteira assinada</span>
            <small>Marque quando ha vinculo formal CLT.</small>
          </span>
        </label>
      </div>
    </fieldset>
  );
}
