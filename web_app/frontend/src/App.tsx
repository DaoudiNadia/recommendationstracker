import React from "react";
import { Routes, Route, Navigate, NavLink } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Recommendation from "./pages/Recommendation";

function App() {
  return (
    <TableProvider>
      <div className="app-container ds-page">
        <header className="ds-nav">
          <div className="ds-container tracker-nav-inner">
            <span className="tracker-brand">Recommendations Tracker</span>
            <nav className="tracker-nav-links" aria-label="Main navigation">
              <NavLink to="/" end className={({ isActive }) => `tracker-nav-link${isActive ? " active" : ""}`}>Home</NavLink>
              <NavLink to="/recommendation" className={({ isActive }) => `tracker-nav-link${isActive ? " active" : ""}`}>Recommendations</NavLink>
              <NavLink to="/recommendation/new" className={({ isActive }) => `tracker-nav-link${isActive ? " active" : ""}`}>Add recommendation</NavLink>
            </nav>
          </div>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Recommendation view="home" />} />
            <Route path="/recommendation" element={<Recommendation view="list" />} />
            <Route path="/recommendation/new" element={<Recommendation view="add" />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
