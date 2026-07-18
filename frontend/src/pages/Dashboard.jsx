import React from 'react';

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from 'recharts';

import {
  CheckCircle2,
  XCircle,
  Lightbulb,
  RotateCcw,
  AlertTriangle,
  Sparkles
} from 'lucide-react';

const COLORS = {
  matched: '#10b981',
  missing: '#ef4444',
  extra: '#6366f1',
};

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

  const coverageData = [
    {
      name: "Matched",
      value: data.matchedSkills.length,
      color: COLORS.matched
    },
    {
      name: "Missing",
      value: data.missingSkills.length,
      color: COLORS.missing
    },
    {
      name: "Extra",
      value: data.extraSkills.length,
      color: COLORS.extra
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-2 animate-in fade-in duration-700">

      <div className="flex justify-between items-center mb-8">

        <h1 className="text-3xl font-bold text-slate-800">
          Analysis Results
        </h1>

        <button
          onClick={onReset}
          className="flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-medium transition"
        >
          <RotateCcw size={18} />
          New Analysis
        </button>

      </div>

      {/* Top Cards */}

      <div className="grid lg:grid-cols-2 gap-6 mb-6">

        {/* ATS Score */}

        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6 flex flex-col items-center">

          <h3 className="text-xs uppercase tracking-widest text-slate-500 font-semibold mb-5">
            Overall ATS Score
          </h3>

          <div className="relative w-44 h-44 flex items-center justify-center">

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
                stroke={getScoreColor(data.score)}
                strokeWidth="12"
                fill="transparent"
                strokeDasharray={503}
                strokeDashoffset={503 - (503 * data.score) / 100}
                strokeLinecap="round"
              />

            </svg>

            <div className="absolute inset-0 flex flex-col items-center justify-center">

              <span className="text-5xl font-black">
                {data.score}
              </span>

              <span className="text-slate-400">
                /100
              </span>

            </div>

          </div>

          <p
            className={`mt-5 font-bold uppercase text-sm ${
              data.score >= 80
                ? "text-emerald-600"
                : data.score >= 50
                ? "text-amber-500"
                : "text-red-500"
            }`}
          >
            {getMatchText(data.score)}
          </p>

          <div className="mt-5 text-center text-sm text-slate-500">

            <p>
              ✓ {data.matchedSkills.length} Skills Matched
            </p>

            <p>
              ✗ {data.missingSkills.length} Skills Missing
            </p>

          </div>

        </div>

        {/* Resume Coverage */}

        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6">

          <div className="flex items-center gap-2 mb-5">

            <Sparkles
              size={20}
              className="text-indigo-600"
            />

            <h3 className="font-bold text-slate-800">
              Resume Coverage
            </h3>

          </div>

          <div className="h-56">

            <ResponsiveContainer width="100%" height="100%">

              <PieChart>

                <Pie
                  data={coverageData}
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={3}
                  dataKey="value"
                >

                  {coverageData.map((item) => (

                    <Cell
                      key={item.name}
                      fill={item.color}
                    />

                  ))}

                </Pie>

              </PieChart>

            </ResponsiveContainer>

          </div>

          <div className="grid grid-cols-3 gap-3 mt-1">

            {coverageData.map((item) => (

              <div
                key={item.name}
                className="rounded-xl bg-slate-50 p-3 text-center border border-slate-100"
              >

                <div
                  className="w-3 h-3 rounded-full mx-auto mb-2"
                  style={{
                    background: item.color
                  }}
                />

                <p className="text-xs text-slate-500">
                  {item.name}
                </p>

                <p className="text-lg font-bold text-slate-800">
                  {item.value}
                </p>

              </div>

            ))}

          </div>

        </div>

      </div>

      {/* Skills */}

            <div className="space-y-6">

        {/* Matched Skills */}

        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">

          <h3 className="font-bold mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-emerald-500" />
            Matched Skills ({data.matchedSkills.length})
          </h3>

          <div className="flex flex-wrap gap-2">

            {data.matchedSkills.map((skill) => (

              <span
                key={skill}
                className="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-sm font-semibold border border-emerald-100"
              >
                {skill}
              </span>

            ))}

          </div>

        </div>

        {/* Missing Skills */}

        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">

          <h3 className="font-bold mb-4 flex items-center gap-2">
            <XCircle className="text-rose-500" />
            Missing Skills ({data.missingSkills.length})
          </h3>

          <div className="flex flex-wrap gap-2">

            {data.missingSkills.map((skill) => (

              <span
                key={skill}
                className="px-3 py-1.5 bg-rose-50 text-rose-700 rounded-full text-sm font-semibold border border-rose-100"
              >
                {skill}
              </span>

            ))}

          </div>

        </div>

        {/* Extra Skills */}

        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">

          <h3 className="font-bold mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-indigo-500" />
            Extra Skills ({data.extraSkills.length})
          </h3>

          <div className="flex flex-wrap gap-2">

            {data.extraSkills.map((skill) => (

              <span
                key={skill}
                className="px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-full text-sm font-semibold border border-indigo-100"
              >
                {skill}
              </span>

            ))}

          </div>

        </div>

        {/* Bottom Layout */}

        <div className="grid lg:grid-cols-3 gap-6">

          {/* Left Side */}

          <div className="lg:col-span-1 space-y-6">

            {/* Strengths */}

            <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">

              <h3 className="font-bold mb-4 flex items-center gap-2">

                <CheckCircle2 className="text-emerald-500" />

                Strengths

              </h3>

              <div className="space-y-2">

                {data.strengths.map((item, index) => (

                  <div
                    key={index}
                    className="p-3 rounded-xl bg-emerald-50 text-emerald-700 text-sm"
                  >
                    {item}
                  </div>

                ))}

              </div>

            </div>

            {/* Weak Areas */}

            <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">

              <h3 className="font-bold mb-4 flex items-center gap-2">

                <AlertTriangle className="text-amber-500" />

                Weak Areas

              </h3>

              <div className="space-y-2">

                {data.weaknesses.map((item, index) => (

                  <div
                    key={index}
                    className="p-3 rounded-xl bg-amber-50 text-amber-700 text-sm"
                  >
                    {item}
                  </div>

                ))}

              </div>

            </div>

          </div>

          {/* Right Side */}

          <div className="lg:col-span-2">

            <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm h-full">

              <h3 className="font-bold mb-5 flex items-center gap-2">

                <Lightbulb className="text-amber-500" />

                Priority Improvements

              </h3>

              <div className="space-y-3">

                {data.aiSuggestions.map((item, index) => (

                  <div
                    key={index}
                    className="p-4 rounded-2xl bg-slate-50 border border-slate-200"
                  >
                    <p className="text-sm leading-6 text-slate-700">
                      {item}
                    </p>
                  </div>

                ))}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
};

export default Dashboard;
