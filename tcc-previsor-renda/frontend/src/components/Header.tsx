// frontend/src/components/Header.tsx
import "./Header.css";
import ifesLogo from "../assets/logo_ifes.png";

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <img
          src={ifesLogo}
          alt="IFES"
          className="logo"
        />
        <div>
          <h1>Previsor de Renda</h1>
          <span>TCC — Sistemas de Informação</span>
        </div>
      </div>
    </header>
  );
}
