// frontend/src/components/Form/LocalizacaoSection.tsx
import { PredictInput } from "../../types/Predict";

interface Props {
  data: PredictInput;
  setData: React.Dispatch<React.SetStateAction<PredictInput>>;
}

export default function LocalizacaoSection({ data, setData }: Props) {
  return (
    <fieldset>
      <legend>Localização</legend>

      <label>
        UF:
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

      <label>
        Zona urbana?
        <input
          type="checkbox"
          checked={data.zona_urbana}
          onChange={(e) =>
            setData({ ...data, zona_urbana: e.target.checked })
          }
        />
      </label>

      <label>
        Região metropolitana?
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
      </label>
    </fieldset>
  );
}
