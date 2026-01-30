// frontend/src/components/Form/DomicilioSection.tsx
import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function DomicilioSection({ data, setData }: Props) {
  return (
    <fieldset>
      <legend>Domicílio</legend>

      <label>
        Total de pessoas:
        <input
          type="number"
          value={data.total_pessoas}
          onChange={(e) =>
            setData({ ...data, total_pessoas: Number(e.target.value) })
          }
        />
      </label>

      <label>
        Quantidade de cômodos:
        <input
          type="number"
          value={data.quantidade_comodos}
          onChange={(e) =>
            setData({
              ...data,
              quantidade_comodos: Number(e.target.value),
            })
          }
        />
      </label>

      <label>
        Quantidade de dormitórios:
        <input
          type="number"
          value={data.quantidade_dormitorios}
          onChange={(e) =>
            setData({
              ...data,
              quantidade_dormitorios: Number(e.target.value),
            })
          }
        />
      </label>

      <label>
        Possui água encanada?
        <input
          type="checkbox"
          checked={data.possui_agua_rede}
          onChange={(e) =>
            setData({ ...data, possui_agua_rede: e.target.checked })
          }
        />
      </label>

      <label>
        Tipo de esgoto:
        <select
          value={data.tipo_esgoto}
          onChange={(e) =>
            setData({ ...data, tipo_esgoto: e.target.value as any })
          }
        >
          <option value="rede">Rede</option>
          <option value="fossa">Fossa</option>
          <option value="outro">Outro</option>
          <option value="nao_informado">Não informado</option>
        </select>
      </label>

      <label>
        Lixo coletado?
        <input
          type="checkbox"
          checked={data.lixo_coletado}
          onChange={(e) =>
            setData({ ...data, lixo_coletado: e.target.checked })
          }
        />
      </label>

      <label>
        Iluminação elétrica?
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
      </label>

      <label>
        Geladeira:
        <input
          type="checkbox"
          checked={data.possui_geladeira}
          onChange={(e) =>
            setData({ ...data, possui_geladeira: e.target.checked })
          }
        />
      </label>

      <label>
        TV:
        <input
          type="checkbox"
          checked={data.possui_tv}
          onChange={(e) =>
            setData({ ...data, possui_tv: e.target.checked })
          }
        />
      </label>

      <label>
        Fogão:
        <input
          type="checkbox"
          checked={data.possui_fogao}
          onChange={(e) =>
            setData({ ...data, possui_fogao: e.target.checked })
          }
        />
      </label>

      <label>
        Rádio:
        <input
          type="checkbox"
          checked={data.possui_radio}
          onChange={(e) =>
            setData({ ...data, possui_radio: e.target.checked })
          }
        />
      </label>
    </fieldset>
  );
}
