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
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#f1ebe2]/90 backdrop-blur-xl border-b border-[#e4dccf] shadow-sm">

      <div className="max-w-7xl mx-auto px-6 py-2 flex items-center justify-between">

        <button
          onClick={() => onNavigate('home')}
          className="flex items-center gap-3"
        >

          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/15">

            <Cpu className="text-white" size={26} />

          </div>

          <span className="font-black text-2xl text-slate-900 tracking-tight">
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
                    ? 'bg-white text-indigo-600 shadow-sm'
                    : 'text-slate-600 hover:bg-white/70 hover:text-slate-900'
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