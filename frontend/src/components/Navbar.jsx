import React from 'react';
import { Cpu, LayoutDashboard, UploadCloud, Home } from 'lucide-react';

export const Navbar = ({ onNavigate, activePage }) => {
  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-slate-200 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => onNavigate('home')}>
          <div className="bg-indigo-600 p-1.5 rounded-lg">
            <Cpu className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-800">BeNobilis</span>
        </div>
        
        <div className="flex gap-8">
          <NavItem active={activePage === 'home'} onClick={() => onNavigate('home')} icon={<Home size={18}/>} label="Home" />
          <NavItem active={activePage === 'upload'} onClick={() => onNavigate('upload')} icon={<UploadCloud size={18}/>} label="Analyze" />
          <NavItem active={activePage === 'dashboard'} onClick={() => onNavigate('dashboard')} icon={<LayoutDashboard size={18}/>} label="Insights" />
        </div>
      </div>
    </nav>
  );
};

const NavItem = ({ active, onClick, icon, label }) => (
  <button 
    onClick={onClick}
    className={`flex items-center gap-2 text-sm font-medium transition-colors ${active ? 'text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}
  >
    {icon} {label}
  </button>
);