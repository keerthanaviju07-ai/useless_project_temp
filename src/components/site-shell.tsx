import { Link, useLocation } from "@tanstack/react-router";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const navItems = [
  { label: "HOME", to: "/" },
  { label: "HOW IT WORKS", to: "/#how-it-works" },
  { label: "THE NODS", to: "/#the-nods" },
] as const;

export function Navbar() {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const homeHref = (hash: string) => (location.pathname === "/" ? hash : `/${hash}`);
  return (
    <header className="site-header">
      <nav className="nav-paper" aria-label="Main navigation">
        <Link to="/" className="brand-mark" onClick={() => setOpen(false)}>
          <span>THALAYATTAM</span>
          <small>TECHNOLOGIES</small>
        </Link>
        <Button
          variant="iconPaper"
          size="icon"
          className="md:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-label={open ? "Close menu" : "Open menu"}
        >
          {open ? <X /> : <Menu />}
        </Button>
        <div className={open ? "nav-links nav-links-open" : "nav-links"}>
          {navItems.map((item) =>
            item.to === "/" ? (
              <Link key={item.label} to="/" onClick={() => setOpen(false)}>{item.label}</Link>
            ) : (
              <a key={item.label} href={homeHref(item.to.slice(1))} onClick={() => setOpen(false)}>{item.label}</a>
            ),
          )}
          <Button asChild variant="scrap" size="sm">
            <Link to="/detect" onClick={() => setOpen(false)}>TRY IT ↗</Link>
          </Button>
        </div>
      </nav>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="scrap-footer">
      <div>
        <strong>THALAYATTAM TECHNOLOGIES</strong>
        <p>Because even a nod needs technology.</p>
      </div>
      <div className="footer-stamp">AI • COMPUTER VISION • MALAYALI NODS</div>
      <p className="font-hand text-lg">Made with questionable amounts of technology. ✦</p>
    </footer>
  );
}