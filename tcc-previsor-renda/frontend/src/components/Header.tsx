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
          <span>Plataforma de previsao de renda | TCC</span>
        </div>
      </div>

      <div className="header-badge">
        <strong>Estimativa inteligente</strong>
        <span>interface institucional do IFES</span>
      </div>
    </header>
  );
}
