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
          <span className="field-label">UF</span>
          <small className="field-hint">Digite a sigla do estado com duas letras.</small>
          <input
            type="text"
            maxLength={2}
            placeholder="Ex: ES"
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
          <span className="switch-copy">
            <span className="switch-label">Zona urbana</span>
            <small>Marque se o domicilio fica em area urbana.</small>
          </span>
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
          <span className="switch-copy">
            <span className="switch-label">Regiao metropolitana</span>
            <small>Marque se pertence a uma regiao metropolitana.</small>
          </span>
        </label>
      </div>
    </fieldset>
  );
}
