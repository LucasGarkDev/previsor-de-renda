// frontend/src/components/Form/DemografiaSection.tsx
import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function DemografiaSection({ data, setData }: Props) {
  return (
    <fieldset>
      <legend>Dados Demográficos</legend>

      <div className="fieldset-grid">
        <label>
          Idade:
          <input
            type="number"
            value={data.idade}
            onChange={(e) =>
              setData({ ...data, idade: Number(e.target.value) })
            }
          />
        </label>

        <label>
          Anos de estudo:
          <input
            type="number"
            value={data.anos_estudo}
            onChange={(e) =>
              setData({ ...data, anos_estudo: Number(e.target.value) })
            }
          />
        </label>

        <label>
          Escolaridade:
          <select
            value={data.ultimo_grau_frequentado}
            onChange={(e) =>
              setData({
                ...data,
                ultimo_grau_frequentado: e.target.value as any,
              })
            }
          >
            <option value="fundamental_incompleto">Fundamental incompleto</option>
            <option value="fundamental_completo">Fundamental completo</option>
            <option value="medio_incompleto">Médio incompleto</option>
            <option value="medio_completo">Médio completo</option>
            <option value="superior_incompleto">Superior incompleto</option>
            <option value="superior_completo">Superior completo</option>
          </select>
        </label>

        <label>
          Sexo:
          <select
            value={data.sexo}
            onChange={(e) =>
              setData({ ...data, sexo: e.target.value as any })
            }
          >
            <option value="masculino">Masculino</option>
            <option value="feminino">Feminino</option>
          </select>
        </label>

        <label>
          Raça/cor:
          <select
            value={data.raca_cor}
            onChange={(e) =>
              setData({ ...data, raca_cor: e.target.value as any })
            }
          >
            <option value="branca">Branca</option>
            <option value="preta">Preta</option>
            <option value="parda">Parda</option>
            <option value="amarela">Amarela</option>
            <option value="indigena">Indígena</option>
          </select>
        </label>
      </div>
    </fieldset>
  );
}
