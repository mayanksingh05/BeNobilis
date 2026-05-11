import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

import {
  CheckCircle2,
  XCircle,
  Lightbulb,
  TrendingUp,
  RotateCcw,
  AlertTriangle
} from 'lucide-react';

const Dashboard = ({ data, onReset }) => {

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getMatchText = (score) => {
    if (score >= 80) return "Great Match";
    if (score >= 50) return "Moderate Match";
    return "Poor Match";
  };

  return (
    <div className="max-w-7xl mx-auto px-6 animate-in fade-in duration-700">

      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">
          Analysis Results
        </h1>

        <button
          onClick={onReset}
          className="flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-medium"
        >
          <RotateCcw size={18} />
          New Analysis
        </button>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">

        <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm flex flex-col items-center justify-center text-center">

          <h3 className="text-slate-500 font-semibold mb-6 uppercase tracking-wider text-xs">
            Overall ATS Score
          </h3>

          <div className="relative w-48 h-48 flex items-center justify-center">

            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="#f1f5f9"
                strokeWidth="12"
                fill="transparent"
              />

              <circle
                cx="96"
                cy="96"
                r="88"
                stroke={getScoreColor(data.score)}
                strokeWidth="12"
                fill="transparent"
                strokeDasharray={553}
                strokeDashoffset={553 - (553 * data.score) / 100}
                strokeLinecap="round"
              />
            </svg>

            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-black text-slate-800">
                {data.score}
              </span>

              <span className="text-slate-400 font-medium">
                / 100
              </span>
            </div>
          </div>

          <p
            className={`mt-6 font-bold flex items-center gap-1 uppercase text-sm ${
              data.score >= 80
                ? "text-emerald-600"
                : data.score >= 50
                ? "text-amber-500"
                : "text-red-500"
            }`}
          >
            <TrendingUp size={16} />
            {getMatchText(data.score)}
          </p>
        </div>

        <div className="lg:col-span-2 bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">

          <h3 className="text-slate-800 font-bold mb-6">
            Skill Category Analysis
          </h3>

          <div className="h-64 w-full">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart data={data.chartData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#f1f5f9"
                />

                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis hide />

                <Tooltip />

                <Bar
                  dataKey="score"
                  radius={[6, 6, 0, 0]}
                  barSize={40}
                >
                  {data.chartData.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={
                        entry.score >= 70
                          ? '#6366f1'
                          : '#cbd5e1'
                      }
                    />
                  ))}
                </Bar>

              </BarChart>

            </ResponsiveContainer>

          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">

            <h3 className="font-bold mb-4 flex items-center gap-2">
              <CheckCircle2 className="text-emerald-500" />
              Matched Skills
            </h3>

            <div className="flex flex-wrap gap-2">

              {data.matchedSkills.map(skill => (
                <span
                  key={skill}
                  className="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-full text-sm font-semibold border border-emerald-100"
                >
                  {skill}
                </span>
              ))}

            </div>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">

            <h3 className="font-bold mb-4 flex items-center gap-2">
              <XCircle className="text-rose-500" />
              Missing Skills
            </h3>

            <div className="flex flex-wrap gap-2">

              {data.missingSkills.map(skill => (
                <span
                  key={skill}
                  className="px-4 py-2 bg-rose-50 text-rose-700 rounded-full text-sm font-semibold border border-rose-100"
                >
                  {skill}
                </span>
              ))}

            </div>
          </div>

        </div>

        <div className="bg-slate-900 text-white p-8 rounded-3xl shadow-xl">

          <h3 className="font-bold mb-6 flex items-center gap-2 text-indigo-400">
            <Lightbulb size={20} />
            AI Suggestions
          </h3>

          <div className="space-y-4">

            {data.aiSuggestions.map((s, i) => (
              <div
                key={i}
                className="p-4 bg-white/5 rounded-2xl border border-white/10"
              >
                <p className="text-slate-300 text-sm">
                  {s}
                </p>
              </div>
            ))}

          </div>
        </div>

        <div className="lg:col-span-3 grid md:grid-cols-2 gap-6">

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">

            <h3 className="font-bold mb-4 flex items-center gap-2">
              <CheckCircle2 className="text-emerald-500" />
              Strengths
            </h3>

            <div className="space-y-3">

              {data.strengths.map((item, index) => (
                <div
                  key={index}
                  className="p-3 rounded-xl bg-emerald-50 text-emerald-700"
                >
                  {item}
                </div>
              ))}

            </div>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">

            <h3 className="font-bold mb-4 flex items-center gap-2">
              <AlertTriangle className="text-amber-500" />
              Weak Areas
            </h3>

            <div className="space-y-3">

              {data.weaknesses.map((item, index) => (
                <div
                  key={index}
                  className="p-3 rounded-xl bg-amber-50 text-amber-700"
                >
                  {item}
                </div>
              ))}

            </div>
          </div>

        </div>

      </div>
    </div>
  );
};

export default Dashboard;