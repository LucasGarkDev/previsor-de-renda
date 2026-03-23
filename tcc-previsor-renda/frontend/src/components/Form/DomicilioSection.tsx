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
          <span>Total de pessoas</span>
          <input
            type="number"
            min={1}
            value={data.total_pessoas}
            onChange={(e) => setData({ ...data, total_pessoas: Number(e.target.value) })}
          />
        </label>

        <label className="field">
          <span>Quantidade de comodos</span>
          <input
            type="number"
            min={0}
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
          <span>Quantidade de dormitorios</span>
          <input
            type="number"
            min={0}
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
          <span>Possui agua encanada</span>
        </label>

        <label className="field">
          <span>Tipo de esgoto</span>
          <select
            value={data.tipo_esgoto}
            onChange={(e) => setData({ ...data, tipo_esgoto: e.target.value as any })}
          >
            <option value="rede">Rede</option>
            <option value="fossa">Fossa</option>
            <option value="outro">Outro</option>
            <option value="nao_informado">Nao informado</option>
          </select>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.lixo_coletado}
            onChange={(e) => setData({ ...data, lixo_coletado: e.target.checked })}
          />
          <span>Lixo coletado</span>
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
          <span>Iluminacao eletrica</span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_geladeira}
            onChange={(e) => setData({ ...data, possui_geladeira: e.target.checked })}
          />
          <span>Possui geladeira</span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_tv}
            onChange={(e) => setData({ ...data, possui_tv: e.target.checked })}
          />
          <span>Possui TV</span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_fogao}
            onChange={(e) => setData({ ...data, possui_fogao: e.target.checked })}
          />
          <span>Possui fogao</span>
        </label>

        <label className="switch-field">
          <input
            type="checkbox"
            checked={data.possui_radio}
            onChange={(e) => setData({ ...data, possui_radio: e.target.checked })}
          />
          <span>Possui radio</span>
        </label>
      </div>
    </fieldset>
  );
}
