import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';
import {
  CheckCircle2,
  XCircle,
  Lightbulb,
  RotateCcw,
  AlertTriangle,
  Sparkles,
  Layers,
  Award
} from 'lucide-react';

const COLORS = {
  matched: '#10b981',
  missing: '#ef4444',
  extra: '#6366f1',
};

const Dashboard = ({ data, onReset }) => {
  if (!data) {
    return (
      <div className="max-w-md mx-auto text-center py-20 px-6">
        <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400">
          <AlertTriangle size={32} />
        </div>
        <h2 className="text-2xl font-bold text-slate-800 mb-2">No Analysis Available</h2>
        <p className="text-slate-500 text-sm mb-6">
          Please upload a resume and job description to view detailed ATS match insights.
        </p>
        <button
          onClick={onReset}
          className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-indigo-700 transition shadow-lg shadow-indigo-100"
        >
          Start New Analysis
        </button>
      </div>
    );
  }

  const score = typeof data.score === 'number' ? data.score : 0;
  const matchedSkills = data.matchedSkills || [];
  const missingSkills = data.missingSkills || [];
  const extraSkills = data.extraSkills || [];
  const strengths = data.strengths || [];
  const weaknesses = data.weaknesses || [];
  const aiSuggestions = data.aiSuggestions || [];
  const chartData = data.chartData || [];

  const getScoreColor = (val) => {
    if (val >= 80) return '#10b981';
    if (val >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getMatchText = (val) => {
    if (val >= 80) return "Great Match";
    if (val >= 50) return "Moderate Match";
    return "Poor Match";
  };

  const coverageData = [
    {
      name: "Matched",
      value: matchedSkills.length,
      color: COLORS.matched
    },
    {
      name: "Missing",
      value: missingSkills.length,
      color: COLORS.missing
    },
    {
      name: "Extra",
      value: extraSkills.length,
      color: COLORS.extra
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-2 animate-in fade-in duration-700">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Analysis Results
          </h1>
          <p className="text-slate-500 text-sm mt-1">
            Hybrid ATS & Semantic NLP Evaluation
          </p>
        </div>

        <button
          onClick={onReset}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-600 hover:text-indigo-600 hover:border-indigo-200 font-medium transition shadow-sm"
        >
          <RotateCcw size={16} />
          New Analysis
        </button>
      </div>

      {/* Top Cards: ATS Score & Overall Coverage */}
      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        {/* ATS Score */}
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6 flex flex-col items-center justify-between">
          <h3 className="text-xs uppercase tracking-widest text-slate-500 font-semibold mb-5 flex items-center gap-2">
            <Award size={16} className="text-indigo-600" />
            Overall ATS Match Score
          </h3>

          <div className="relative w-44 h-44 flex items-center justify-center my-2">
            <svg className="w-full h-full -rotate-90">
              <circle
                cx="88"
                cy="88"
                r="80"
                stroke="#f1f5f9"
                strokeWidth="12"
                fill="transparent"
              />
              <circle
                cx="88"
                cy="88"
                r="80"
                stroke={getScoreColor(score)}
                strokeWidth="12"
                fill="transparent"
                strokeDasharray={503}
                strokeDashoffset={503 - (503 * score) / 100}
                strokeLinecap="round"
              />
            </svg>

            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-black text-slate-800">
                {score}
              </span>
              <span className="text-slate-400 text-xs font-semibold">
                OUT OF 100
              </span>
            </div>
          </div>

          <div className="text-center mt-3">
            <span
              className={`font-bold uppercase text-sm px-3 py-1 rounded-full ${
                score >= 80
                  ? "bg-emerald-50 text-emerald-600"
                  : score >= 50
                  ? "bg-amber-50 text-amber-600"
                  : "bg-rose-50 text-rose-600"
              }`}
            >
              {getMatchText(score)}
            </span>

            <div className="mt-4 flex items-center justify-center gap-6 text-xs text-slate-500">
              <span className="text-emerald-600 font-medium">✓ {matchedSkills.length} Matched</span>
              <span className="text-rose-500 font-medium">✗ {missingSkills.length} Missing</span>
              <span className="text-indigo-600 font-medium">+ {extraSkills.length} Extra</span>
            </div>
          </div>
        </div>

        {/* Resume Coverage Donut */}
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6 flex flex-col justify-between">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles size={18} className="text-indigo-600" />
            <h3 className="font-bold text-slate-800">
              Skill Alignment Ratio
            </h3>
          </div>

          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={coverageData}
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {coverageData.map((item) => (
                    <Cell key={item.name} fill={item.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-3 mt-2">
            {coverageData.map((item) => (
              <div
                key={item.name}
                className="rounded-xl bg-slate-50 p-2.5 text-center border border-slate-100"
              >
                <div
                  className="w-2.5 h-2.5 rounded-full mx-auto mb-1.5"
                  style={{ background: item.color }}
                />
                <p className="text-xs text-slate-500">{item.name}</p>
                <p className="text-lg font-bold text-slate-800">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Skill Category Breakdown (Feature Gap Resolved) */}
      {chartData && chartData.length > 0 && (
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Layers size={20} className="text-indigo-600" />
              <h3 className="font-bold text-slate-800 text-lg">
                Skill Category Breakdown
              </h3>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
              {chartData.length} Domains Analyzed
            </span>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {chartData.map((cat) => {
              const total = cat.matched + cat.missing;
              const matchPercent = total > 0 ? Math.round((cat.matched / total) * 100) : 100;

              return (
                <div
                  key={cat.category}
                  className="p-4 rounded-2xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-semibold text-sm text-slate-800">
                      {cat.category}
                    </span>
                    <span className="text-xs font-bold text-slate-500">
                      {matchPercent}% Match
                    </span>
                  </div>

                  {/* Progress bar */}
                  <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden flex mb-3">
                    <div
                      style={{ width: `${matchPercent}%` }}
                      className="bg-emerald-500 h-full"
                    />
                    <div
                      style={{ width: `${100 - matchPercent}%` }}
                      className="bg-rose-400 h-full"
                    />
                  </div>

                  <div className="flex justify-between text-xs text-slate-500 font-medium">
                    <span className="text-emerald-700">✓ {cat.matched} Matched</span>
                    <span className="text-rose-600">✗ {cat.missing} Missing</span>
                    {cat.extra > 0 && (
                      <span className="text-indigo-600">+{cat.extra} Extra</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Skills Lists */}
      <div className="space-y-6 mb-6">
        {/* Matched Skills */}
        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
          <h3 className="font-bold mb-4 flex items-center gap-2 text-slate-800">
            <CheckCircle2 className="text-emerald-500" />
            Matched Skills ({matchedSkills.length})
          </h3>
          {matchedSkills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {matchedSkills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-sm font-semibold border border-emerald-100 shadow-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400 italic">No direct keyword matches found with the job description.</p>
          )}
        </div>

        {/* Missing Skills */}
        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
          <h3 className="font-bold mb-4 flex items-center gap-2 text-slate-800">
            <XCircle className="text-rose-500" />
            Missing Skills ({missingSkills.length})
          </h3>
          {missingSkills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {missingSkills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1.5 bg-rose-50 text-rose-700 rounded-full text-sm font-semibold border border-rose-100 shadow-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-emerald-600 font-medium">All technical skills in the job description are covered!</p>
          )}
        </div>

        {/* Extra Skills */}
        {extraSkills.length > 0 && (
          <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
            <h3 className="font-bold mb-4 flex items-center gap-2 text-slate-800">
              <Sparkles className="text-indigo-500" />
              Additional Resume Skills ({extraSkills.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {extraSkills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-full text-sm font-semibold border border-indigo-100 shadow-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Bottom Layout: Strengths, Weaknesses, and Priority Improvements */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Side: Strengths & Weaknesses */}
        <div className="lg:col-span-1 space-y-6">
          {/* Strengths */}
          <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
            <h3 className="font-bold mb-4 flex items-center gap-2 text-slate-800">
              <CheckCircle2 className="text-emerald-500" />
              Key Strengths
            </h3>
            <div className="space-y-2.5">
              {strengths.length > 0 ? (
                strengths.map((item, index) => (
                  <div
                    key={index}
                    className="p-3 rounded-xl bg-emerald-50/80 text-emerald-800 text-sm font-medium border border-emerald-100"
                  >
                    {item}
                  </div>
                ))
              ) : (
                <div className="p-3 rounded-xl bg-slate-50 text-slate-600 text-sm">
                  Foundational technical profile detected.
                </div>
              )}
            </div>
          </div>

          {/* Weak Areas */}
          <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
            <h3 className="font-bold mb-4 flex items-center gap-2 text-slate-800">
              <AlertTriangle className="text-amber-500" />
              Areas for Improvement
            </h3>
            <div className="space-y-2.5">
              {weaknesses.length > 0 ? (
                weaknesses.map((item, index) => (
                  <div
                    key={index}
                    className="p-3 rounded-xl bg-amber-50/80 text-amber-800 text-sm font-medium border border-amber-100"
                  >
                    {item}
                  </div>
                ))
              ) : (
                <div className="p-3 rounded-xl bg-slate-50 text-slate-600 text-sm">
                  No critical gaps identified for this role.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Side: Actionable Recommendations */}
        <div className="lg:col-span-2">
          <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm h-full flex flex-col">
            <h3 className="font-bold mb-5 flex items-center gap-2 text-slate-800 text-lg">
              <Lightbulb className="text-amber-500" />
              Priority ATS Optimization Recommendations
            </h3>

            <div className="space-y-3.5 flex-1">
              {aiSuggestions.map((item, index) => (
                <div
                  key={index}
                  className="p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-indigo-200 transition"
                >
                  <p className="text-sm leading-relaxed text-slate-700 font-medium">
                    {item}
                  </p>
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

