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
          <h1>Previsor de Renda</h1>
          <span>TCC | Sistemas de Informacao</span>
        </div>
      </div>

      <div className="header-badge">
        <strong>Frontend renovado</strong>
        <span>mais legivel, dinamico e responsivo</span>
      </div>
    </header>
  );
}
