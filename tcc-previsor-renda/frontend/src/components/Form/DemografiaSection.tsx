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
          <span className="field-label">Idade</span>
          <small className="field-hint">Informe a idade em anos completos.</small>
          <input
            type="number"
            min={18}
            max={100}
            placeholder="Ex: 30"
            value={data.idade}
            onChange={(e) => setData({ ...data, idade: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span className="field-label">Anos de estudo</span>
          <small className="field-hint">Conte apenas anos concluidos, de 0 a 17.</small>
          <input
            type="number"
            min={0}
            max={17}
            placeholder="Ex: 11"
            value={data.anos_estudo}
            onChange={(e) => setData({ ...data, anos_estudo: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span className="field-label">Escolaridade</span>
          <small className="field-hint">Maior nivel de ensino que a pessoa cursou.</small>
          <select
            value={data.ultimo_grau_frequentado}
            onChange={(e) =>
              setData({
                ...data,
                ultimo_grau_frequentado: e.target.value as any,
              })
            }
          >
            <optgroup label="Maior grau cursado">
              <option value="fundamental_incompleto">Fundamental incompleto</option>
              <option value="fundamental_completo">Fundamental completo</option>
              <option value="medio_incompleto">Medio incompleto</option>
              <option value="medio_completo">Medio completo</option>
              <option value="superior_incompleto">Superior incompleto</option>
              <option value="superior_completo">Superior completo</option>
            </optgroup>
          </select>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.sabe_ler_escrever}
            onChange={(e) =>
              setData({ ...data, sabe_ler_escrever: e.target.checked })
            }
          />
          <span className="switch-copy">
            <span className="switch-label">Sabe ler e escrever</span>
            <small>Marque quando a pessoa e alfabetizada.</small>
          </span>
        </label>

        <label className="field">
          <span className="field-label">Sexo</span>
          <small className="field-hint">Selecione a opcao informada na pesquisa.</small>
          <select
            value={data.sexo}
            onChange={(e) => setData({ ...data, sexo: e.target.value as any })}
          >
            <optgroup label="Opcao informada">
              <option value="masculino">Masculino</option>
              <option value="feminino">Feminino</option>
            </optgroup>
          </select>
        </label>

        <label className="field">
          <span className="field-label">Raca/cor</span>
          <small className="field-hint">Use a autodeclaracao da pessoa.</small>
          <select
            value={data.raca_cor}
            onChange={(e) => setData({ ...data, raca_cor: e.target.value as any })}
          >
            <optgroup label="Autodeclaracao">
              <option value="branca">Branca</option>
              <option value="preta">Preta</option>
              <option value="parda">Parda</option>
              <option value="amarela">Amarela</option>
              <option value="indigena">Indigena</option>
            </optgroup>
          </select>
        </label>
      </div>
    </fieldset>
  );
}
