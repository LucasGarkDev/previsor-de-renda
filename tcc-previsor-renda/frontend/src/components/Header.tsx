import "./Header.css";
import ifesLogo from "../assets/logo_ifes.png";

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <div className="logo-shell">
          <img src={ifesLogo} alt="IFES" className="logo" />
        </div>
        <div>
          <h1>IFES Previsor de Renda</h1>
          <span>Simulador socioeconomico para apoio academico</span>
        </div>
      </div>

      <div className="header-badge">
        <strong>TCC</strong>
        <span>modelo Mincer + CatBoost</span>
      </div>
    </header>
  );
}
