import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Zap, Shield, BarChart3, ArrowRight, Cpu } from 'lucide-react';

const Home = ({ onStart }) => {
  return (
    <div className="max-w-7xl mx-auto px-6">
      <section className="py-20 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <span className="px-4 py-1.5 rounded-full bg-indigo-50 text-indigo-600 text-sm font-semibold mb-6 inline-block border border-indigo-100">
            Next-Gen Career Intelligence
          </span>
          <h1 className="text-6xl font-extrabold text-slate-900 mb-6 tracking-tight leading-tight">
            Elevate your career with <br/> <span className="text-indigo-600">AI-powered</span> resume intelligence.
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto mb-10">
            BeNobilis uses advanced NLP to bridge the gap between your talent and your dream job. Get ATS-optimized feedback in seconds.
          </p>
          <button 
            onClick={onStart}
            className="bg-slate-900 text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-slate-800 transition-all flex items-center gap-2 mx-auto shadow-xl shadow-slate-200"
          >
            Analyze Your Resume <ArrowRight size={20} />
          </button>
        </motion.div>
      </section>

      <section className="grid md:grid-cols-4 gap-8 py-20">
        <FeatureCard icon={<BarChart3 className="text-indigo-600"/>} title="ATS Scoring" desc="See exactly how applicant tracking systems rank your profile." />
        <FeatureCard icon={<Zap className="text-amber-500"/>} title="Skill Gap" desc="Identify missing keywords and technical skills recruiters want." />
        <FeatureCard icon={<Cpu className="text-emerald-500"/>} title="AI Suggestions" desc="Get ChatGPT-style rewrites for your experience bullet points." />
        <FeatureCard icon={<CheckCircle className="text-blue-500"/>} title="Job Matching" desc="Compare your resume against specific job descriptions." />
      </section>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }) => (
  <div className="p-8 bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
    <div className="mb-4">{icon}</div>
    <h3 className="text-lg font-bold mb-2">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
  </div>
);

export default Home;