// frontend/src/components/Form/TrabalhoSection.tsx
import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function TrabalhoSection({ data, setData }: Props) {
  return (
    <fieldset>
      <legend>Trabalho</legend>

      <label>
        Trabalhou na última semana?
        <input
          type="checkbox"
          checked={data.trabalhou_semana}
          onChange={(e) =>
            setData({ ...data, trabalhou_semana: e.target.checked })
          }
        />
      </label>

      <label>
        Horas trabalhadas por semana:
        <input
          type="number"
          value={data.horas_trabalhadas_semana}
          onChange={(e) =>
            setData({
              ...data,
              horas_trabalhadas_semana: Number(e.target.value),
            })
          }
        />
      </label>

      <label>
        Está ocupado atualmente?
        <input
          type="checkbox"
          checked={data.ocupacao_semana}
          onChange={(e) =>
            setData({ ...data, ocupacao_semana: e.target.checked })
          }
        />
      </label>

      <label>
        Ramo de atividade (código PNAD):
        <input
          type="number"
          value={data.atividade_ramo_negocio_semana}
          onChange={(e) =>
            setData({
              ...data,
              atividade_ramo_negocio_semana: Number(e.target.value),
            })
          }
        />
      </label>

      <label>
        Posição na ocupação:
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
          <option value="conta_propria">Conta própria</option>
          <option value="outro">Outro</option>
        </select>
      </label>

      <label>
        Possui carteira assinada?
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
      </label>
    </fieldset>
  );
}
