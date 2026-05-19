import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function DomicilioSection({ data, setData }: Props) {
  return (
    <fieldset className="form-section">
      <legend>Domicilio</legend>
      <p className="section-description">
        Estrutura da residencia, servicos basicos e bens do domicilio.
      </p>

      <div className="fieldset-grid">
        <label className="field">
          <span className="field-label">Total de pessoas</span>
          <small className="field-hint">Moradores que vivem no domicilio.</small>
          <input
            type="number"
            min={1}
            placeholder="Ex: 4"
            value={data.total_pessoas}
            onChange={(e) => setData({ ...data, total_pessoas: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span className="field-label">Quantidade de comodos</span>
          <small className="field-hint">Total de ambientes da residencia.</small>
          <input
            type="number"
            min={1}
            placeholder="Ex: 5"
            value={data.quantidade_comodos}
            onChange={(e) =>
              setData({
                ...data,
                quantidade_comodos: Number(e.target.value),
              })
            }
          />
        </label>

        <label className="field">
          <span className="field-label">Quantidade de dormitorios</span>
          <small className="field-hint">Quartos usados para dormir.</small>
          <input
            type="number"
            min={0}
            placeholder="Ex: 2"
            value={data.quantidade_dormitorios}
            onChange={(e) =>
              setData({
                ...data,
                quantidade_dormitorios: Number(e.target.value),
              })
            }
          />
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_agua_rede}
            onChange={(e) => setData({ ...data, possui_agua_rede: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Possui agua encanada</span>
            <small>Marque se a agua vem por rede geral.</small>
          </span>
        </label>

        <label className="field">
          <span className="field-label">Tipo de esgoto</span>
          <small className="field-hint">Principal forma de esgotamento sanitario.</small>
          <select
            value={data.tipo_esgoto}
            onChange={(e) => setData({ ...data, tipo_esgoto: e.target.value as any })}
          >
            <optgroup label="Forma principal">
              <option value="rede">Rede geral</option>
              <option value="fossa">Fossa</option>
              <option value="outro">Outro</option>
              <option value="nao_informado">Nao informado</option>
            </optgroup>
          </select>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.lixo_coletado}
            onChange={(e) => setData({ ...data, lixo_coletado: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Lixo coletado</span>
            <small>Marque se ha coleta direta ou indireta de lixo.</small>
          </span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_iluminacao_eletrica}
            onChange={(e) =>
              setData({
                ...data,
                possui_iluminacao_eletrica: e.target.checked,
              })
            }
          />
          <span className="switch-copy">
            <span className="switch-label">Iluminacao eletrica</span>
            <small>Marque se o domicilio possui energia eletrica.</small>
          </span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_geladeira}
            onChange={(e) => setData({ ...data, possui_geladeira: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Possui geladeira</span>
            <small>Considere geladeira em funcionamento.</small>
          </span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_tv}
            onChange={(e) => setData({ ...data, possui_tv: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Possui TV</span>
            <small>Marque se ha televisao no domicilio.</small>
          </span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_fogao}
            onChange={(e) => setData({ ...data, possui_fogao: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Possui fogao</span>
            <small>Marque se ha fogao ou equipamento equivalente.</small>
          </span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_radio}
            onChange={(e) => setData({ ...data, possui_radio: e.target.checked })}
          />
          <span className="switch-copy">
            <span className="switch-label">Possui radio</span>
            <small>Marque se ha radio no domicilio.</small>
          </span>
        </label>
      </div>
    </fieldset>
  );
}
