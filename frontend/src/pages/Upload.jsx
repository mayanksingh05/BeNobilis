import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Briefcase, Loader2, Check } from 'lucide-react';

const UploadPage = ({ onAnalyze }) => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [step, setStep] = useState(0);

  const steps = ["Extracting Text", "Analyzing Skills", "Scoring against JD", "Generating Insights"];

  const handleUpload = () => {
    if (!file || !jobDescription) return alert("Please provide both a resume and a JD.");
    
    setIsAnalyzing(true);
    // Simulate API calls with intervals
    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < steps.length - 1) {
        setStep(prev => prev + 1);
        currentStep++;
      } else {
        clearInterval(interval);
        // Mock Response Data
        onAnalyze({
          score: 82,
          matchedSkills: ['React.js', 'Tailwind CSS', 'Node.js', 'REST APIs', 'Git'],
          missingSkills: ['AWS Deployment', 'Docker', 'GraphQL', 'Unit Testing'],
          strengths: ['Strong project leadership', 'Modern tech stack proficiency', 'Clean code practices'],
          weaknesses: ['Lack of cloud infrastructure experience', 'Few quantifiable metrics in experience section'],
          aiSuggestions: [
            "Quantify your React projects: 'Improved load times by 40%' instead of 'Built fast apps'.",
            "Add a specific section for DevOps tools to improve ATS score for Senior roles."
          ]
        });
      }
    }, 1500);
  };

  return (
    <div className="max-w-6xl mx-auto px-6">
      <div className="grid lg:grid-cols-2 gap-12 items-start">
        {/* Left: Resume Upload */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <FileText className="text-indigo-600" /> Resume Upload
          </h2>
          <div 
            className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${file ? 'border-emerald-400 bg-emerald-50' : 'border-slate-200 bg-white hover:border-indigo-400'}`}
          >
            <input 
              type="file" 
              id="resume" 
              className="hidden" 
              onChange={(e) => setFile(e.target.files[0])} 
              accept=".pdf"
            />
            <label htmlFor="resume" className="cursor-pointer">
              <div className="bg-slate-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Upload className="text-slate-500" />
              </div>
              {file ? (
                <p className="text-emerald-700 font-medium">{file.name}</p>
              ) : (
                <>
                  <p className="font-bold text-slate-700 text-lg">Click to upload or drag and drop</p>
                  <p className="text-slate-400 text-sm mt-1">PDF files only (Max 5MB)</p>
                </>
              )}
            </label>
          </div>
        </div>

        {/* Right: JD Input */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Briefcase className="text-indigo-600" /> Job Description
          </h2>
          <textarea 
            placeholder="Paste the job description here to see how well you match..."
            className="w-full h-64 p-6 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none bg-white shadow-sm"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <button 
            disabled={isAnalyzing}
            onClick={handleUpload}
            className="w-full bg-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100 flex items-center justify-center gap-3"
          >
            {isAnalyzing ? <Loader2 className="animate-spin" /> : "Analyze Match"}
          </button>
        </div>
      </div>

      {/* Loading Overlay */}
      <AnimatePresence>
        {isAnalyzing && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[60] flex items-center justify-center"
          >
            <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-sm w-full text-center">
              <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-6" />
              <h3 className="text-xl font-bold mb-8">AI Analysis in Progress</h3>
              <div className="space-y-4">
                {steps.map((s, i) => (
                  <div key={i} className={`flex items-center gap-3 text-sm ${i <= step ? 'text-slate-900' : 'text-slate-300'}`}>
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center border ${i < step ? 'bg-emerald-500 border-emerald-500' : 'border-slate-300'}`}>
                      {i < step && <Check size={12} className="text-white" />}
                    </div>
                    <span className={i === step ? "font-bold text-indigo-600" : ""}>{s}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UploadPage;