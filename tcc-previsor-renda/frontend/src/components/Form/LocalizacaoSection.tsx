import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function LocalizacaoSection({ data, setData }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Localizacao</legend>
      <p className="section-description">
        Localidade e caracteristicas urbanas da residencia.
      </p>

      <div className="fieldset-grid">
        <label className="field">
          <span>UF</span>
          <input
            type="text"
            maxLength={2}
            value={data.sigla_uf}
            onChange={(e) =>
              setData({
                ...data,
                sigla_uf: e.target.value.toUpperCase(),
              })
            }
          />
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.zona_urbana}
            onChange={(e) => setData({ ...data, zona_urbana: e.target.checked })}
          />
          <span>Zona urbana</span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.regiao_metropolitana}
            onChange={(e) =>
              setData({
                ...data,
                regiao_metropolitana: e.target.checked,
              })
            }
          />
          <span>Regiao metropolitana</span>
        </label>
      </div>
    </fieldset>
  );
}
