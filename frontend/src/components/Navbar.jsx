import React from 'react';
import {
  Cpu,
  Home,
  Upload
} from 'lucide-react';

export const Navbar = ({ onNavigate, activePage }) => {

  const navItems = [
    {
      id: 'home',
      label: 'Home',
      icon: Home
    },
    {
      id: 'upload',
      label: 'Analyze',
      icon: Upload
    }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-100">

      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        <button
          onClick={() => onNavigate('home')}
          className="flex items-center gap-3"
        >

          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">

            <Cpu className="text-white" size={26} />

          </div>

          <span className="font-black text-2xl text-slate-800 tracking-tight">
            BeNobilis
          </span>

        </button>

        <nav className="hidden md:flex items-center gap-2">

          {navItems.map((item) => {

            const Icon = item.icon;

            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  activePage === item.id
                    ? 'bg-indigo-50 text-indigo-600'
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >

                <Icon size={18} />

                {item.label}

              </button>
            );
          })}

        </nav>

      </div>

    </header>
  );
};