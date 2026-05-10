import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Dashboard from './pages/Dashboard';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [analysisData, setAnalysisData] = useState(null);

  const navigateTo = (page) => setCurrentPage(page);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setCurrentPage('dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-indigo-100">
      <Navbar onNavigate={navigateTo} activePage={currentPage} />

      <main className="pt-20 pb-12">
        {currentPage === 'home' && <Home onStart={() => setCurrentPage('upload')} />}
        {currentPage === 'upload' && <Upload onAnalyze={handleAnalysisComplete} />}
        {currentPage === 'dashboard' && <Dashboard data={analysisData} onReset={() => setCurrentPage('upload')} />}
      </main>
    </div>
  );
}

export default App;