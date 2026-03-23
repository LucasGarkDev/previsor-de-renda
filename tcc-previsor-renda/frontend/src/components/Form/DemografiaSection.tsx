import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function DemografiaSection({ data, setData }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Dados Demograficos</legend>
      <p className="section-description">
        Perfil basico de identificacao e escolaridade.
      </p>

      <div className="fieldset-grid">
        <label className="field">
          <span>Idade</span>
          <input
            type="number"
            min={0}
            value={data.idade}
            onChange={(e) => setData({ ...data, idade: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span>Anos de estudo</span>
          <input
            type="number"
            min={0}
            value={data.anos_estudo}
            onChange={(e) => setData({ ...data, anos_estudo: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span>Escolaridade</span>
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
            <option value="medio_incompleto">Medio incompleto</option>
            <option value="medio_completo">Medio completo</option>
            <option value="superior_incompleto">Superior incompleto</option>
            <option value="superior_completo">Superior completo</option>
          </select>
        </label>

        <label className="field">
          <span>Sexo</span>
          <select
            value={data.sexo}
            onChange={(e) => setData({ ...data, sexo: e.target.value as any })}
          >
            <option value="masculino">Masculino</option>
            <option value="feminino">Feminino</option>
          </select>
        </label>

        <label className="field">
          <span>Raca/cor</span>
          <select
            value={data.raca_cor}
            onChange={(e) => setData({ ...data, raca_cor: e.target.value as any })}
          >
            <option value="branca">Branca</option>
            <option value="preta">Preta</option>
            <option value="parda">Parda</option>
            <option value="amarela">Amarela</option>
            <option value="indigena">Indigena</option>
          </select>
        </label>
      </div>
    </fieldset>
  );
}
