"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, ReferenceLine, 
  Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, Cell 
} from "recharts";

const Clock = () => {
  const [currentTime, setCurrentTime] = useState<string>("");
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const options: Intl.DateTimeFormatOptions = {
        timeZone: "Asia/Kolkata",
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false
      };
      
      const parts = new Intl.DateTimeFormat('en-GB', options).formatToParts(now);
      const _ = (type: string) => parts.find(p => p.type === type)?.value || "";
      const hourNum = parseInt(_('hour'), 10);
      const ampm = hourNum >= 12 ? 'pm' : 'am';
      const formatted = `${_('day')}/${_('month')}/${_('year')}, ${_('hour')}:${_('minute')}:${_('second')} ${ampm} +5:30`;
      
      setCurrentTime(formatted);
    };
    
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);
  return <>{currentTime}</>;
};

export default function CreditRiskEngine() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [showJson, setShowJson] = useState(false);
  const [userId, setUserId] = useState<string>("");

  const [formData, setFormData] = useState({
    fullName: "Ramesh Naik",
    pan: "PQRSX9876L",
    amount: "50000"
  });
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    setUserId(crypto.randomUUID());
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const parseCSV = (text: string) => {
    const lines = text.split('\n');
    const result = [];
    const headers = lines[0].split(',').map(h => h.trim());
    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;
        const obj: any = {};
        const currentline = lines[i].split(',');
        for (let j = 0; j < headers.length; j++) {
            obj[headers[j]] = currentline[j] ? currentline[j].trim() : '';
        }
        result.push(obj);
    }
    return result;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload a transaction CSV.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onload = async function(event) {
      const csvText = event.target?.result as string;
      const transactionData = parseCSV(csvText);

      const payload = {
          user_id: userId || crypto.randomUUID(), 
          pan: formData.pan.trim(),
          aadhaar: null, 
          full_name: formData.fullName.trim(),
          amount: parseFloat(formData.amount),
          transaction_data: transactionData
      };

      try {
          const apiBase = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';
          const response = await fetch(`${apiBase}/apply`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
          });
          
          const data = await response.json();

          if (!response.ok) {
              const errorDetail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
              throw new Error(errorDetail || `HTTP Error ${response.status}`);
          }
          
          if (data.shap_values) {
              data.shapChartData = Object.entries(data.shap_values).map(([key, value]) => ({
                  parameter: key,
                  impact: value as number,
                  absImpact: Math.abs(value as number)
              }));
          }

          setResult(data);

      } catch (err: any) {
          setError(err.message);
      } finally {
          setLoading(false);
      }
    };
    reader.readAsText(file);
  };

  // Gradient offset calculation
  const calculateGradientOffset = (chartData: any[]) => {
    if (!chartData || chartData.length === 0) return 0;
    const max = Math.max(...chartData.map(d => d.impact));
    const min = Math.min(...chartData.map(d => d.impact));
    
    if (min >= 0) return 0;   // All positive (above zero -> Red)
    if (max <= 0) return 1;   // All negative (below zero -> Green)
    
    // Formula calculates where the 0 falls as a percentage from top (max) to bottom (min)
    return max / (max - min);
  };
  
  const gradientOffset = result?.shapChartData ? calculateGradientOffset(result.shapChartData) : 0;
  
  // Custom multi-colors for Parameter Chart
  const BAR_COLORS = [
    '#3b82f6', '#ec4899', '#f59e0b', '#10b981', '#a855f7', '#06b6d4', '#ef4444', '#eab308'
  ];

  return (
    <div className="h-screen w-screen overflow-hidden bg-[#0d0d0d] text-zinc-100 font-mono p-4 md:p-6 flex flex-col items-center">
      <div className="w-full max-w-[1400px] h-full flex flex-col flex-1 min-h-0 gap-4">
        
        {/* Header section with Title and Date/Time */}
        <div className="flex justify-between items-center mb-2 w-full">
          <h1 className="text-xl md:text-2xl font-bold uppercase tracking-widest text-zinc-100">
            Explainable Credit Engine
          </h1>
          
          <div className="border border-zinc-800 rounded bg-[#16161A] px-4 py-2 text-xs font-medium tracking-wide text-zinc-400">
            <Clock />
          </div>
        </div>

        {/* Main 3-column Grid mimicking the high-fidelity screenshot */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 flex-1 min-h-0 w-full">
          
          {/* LEFT COLUMN: Loan App Form (span 3/12) */}
          <div className="lg:col-span-3 border border-zinc-800 bg-[#121215] rounded-xl p-5 flex flex-col min-h-0 overflow-y-auto">
            <h2 className="text-sm font-bold uppercase tracking-widest border-b border-zinc-800 pb-3 mb-6 flex justify-between">
              Loan Application Form
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4 flex-1 flex flex-col">
              <div className="space-y-2">
                <Label className="uppercase text-[10px] text-zinc-500 font-bold tracking-widest" htmlFor="userId">Application ID (UUID)</Label>
                <Input 
                  id="userId" 
                  value={userId} 
                  disabled
                  readOnly
                  className="bg-[#1a1a1e] border-zinc-800/50 rounded h-11 text-xs px-3 text-zinc-600 font-mono transition-colors opacity-80 cursor-not-allowed"
                />
              </div>
              <div className="space-y-2">
                <Label className="uppercase text-[10px] text-zinc-500 font-bold tracking-widest" htmlFor="fullName">Full Name</Label>
                <Input 
                  id="fullName" 
                  name="fullName" 
                  value={formData.fullName} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-[#1C1C20] border-zinc-800/80 rounded h-11 text-xs px-3 focus-visible:ring-1 focus-visible:ring-zinc-600 text-zinc-300 transition-colors"
                />
              </div>
              <div className="space-y-2">
                <Label className="uppercase text-[10px] text-zinc-500 font-bold tracking-widest" htmlFor="pan">PAN</Label>
                <Input 
                  id="pan" 
                  name="pan" 
                  value={formData.pan} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-[#1C1C20] border-zinc-800/80 rounded h-11 text-xs px-3 focus-visible:ring-1 focus-visible:ring-zinc-600 text-zinc-300 transition-colors uppercase"
                />
              </div>
              <div className="space-y-2">
                <Label className="uppercase text-[10px] text-zinc-500 font-bold tracking-widest" htmlFor="amount">Loan Amount</Label>
                <Input 
                  id="amount" 
                  name="amount" 
                  type="number" 
                  value={formData.amount} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-[#1C1C20] border-zinc-800/80 rounded h-11 text-xs px-3 focus-visible:ring-1 focus-visible:ring-zinc-600 text-zinc-300 transition-colors"
                />
              </div>
              <div className="space-y-2 pt-2">
                <Label className="uppercase text-[10px] text-zinc-500 font-bold tracking-widest inline-block mb-1" htmlFor="file">Upload Transaction Data (CSV)</Label>
                <Input 
                  id="file" 
                  type="file" 
                  accept=".csv" 
                  onChange={handleFileChange} 
                  required 
                  className="bg-[#1C1C20]/50 border-zinc-700 border-dashed rounded h-12 pt-3 px-3 cursor-pointer text-[10px] text-zinc-400 focus-visible:ring-0 file:hidden"
                />
              </div>
              
              <div className="py-2">
                <Button type="submit" className="w-full text-base h-12 bg-zinc-100 hover:bg-white text-black font-bold uppercase tracking-widest rounded-full transition-all active:scale-95" disabled={loading}>
                  {loading ? "Analyzing..." : "Submit"}
                </Button>
                {error && <div className="mt-3 text-[#ff4b4b] text-[10px] text-center">{error}</div>}
              </div>
            </form>
          </div>

          {/* CENTER COLUMN: The Probability Curve (span 6/12) */}
          <div className="lg:col-span-6 flex flex-col gap-5 relative min-h-0 min-w-0">
            
            {/* Top Status Indicators (Approved/Rejected + Prob) */}
            <div className="flex gap-5">
              <div className="border border-zinc-800 rounded-xl bg-[#17171d] px-6 py-4 flex flex-1 items-center justify-center gap-3 shadow-md">
                {result ? (
                  result.decision === 'APPROVED' ? (
                     <div className="flex items-center gap-3">
                       <div className="w-5 h-5 bg-[#4ADE80] flex items-center justify-center rounded-[3px] text-black">✓</div>
                       <span className="text-xl font-bold tracking-widest uppercase text-zinc-100 whitespace-nowrap">APPROVED</span>
                     </div>
                  ) : (
                     <div className="flex items-center gap-3">
                       <div className="w-5 h-5 bg-[#EF4444] flex items-center justify-center rounded-[3px] text-white">X</div>
                       <span className="text-xl font-bold tracking-widest uppercase text-zinc-100 whitespace-nowrap">REJECTED</span>
                     </div>
                  )
                ) : loading ? (
                  <span className="text-xl font-bold tracking-widest uppercase text-zinc-300">EVALUATING...</span>
                ) : (
                  <span className="text-xl font-bold tracking-widest uppercase text-zinc-600">STATUS</span>
                )}
              </div>
              
              <div className="border border-zinc-800 rounded-xl bg-[#121215] px-6 py-4 flex flex-col flex-1 items-center justify-center shadow-md">
                <span className="text-[9px] uppercase font-bold text-zinc-500 tracking-widest leading-none mb-2">Approval Prob.</span>
                <span className={`text-3xl font-bold leading-none tracking-wider ${result ? (result.decision === 'APPROVED' ? 'text-[#4ADE80]' : 'text-[#EF4444]') : 'text-zinc-600'}`}>
                  {result ? `${(result.approval_probability * 100).toFixed(1)}%` : "--%"}
                </span>
              </div>

              <div className="border border-zinc-800 rounded-xl bg-[#121215] px-6 py-4 flex flex-col flex-1 items-center justify-center shadow-md">
                <span className="text-[9px] uppercase font-bold text-zinc-500 tracking-widest leading-none mb-2">Risk Score</span>
                <span className={`text-3xl font-bold leading-none tracking-wider ${result ? (result.decision === 'APPROVED' ? 'text-zinc-400' : 'text-[#EF4444]') : 'text-zinc-600'}`}>
                  {result ? `${(result.default_probability * 100).toFixed(1)}%` : "--%"}
                </span>
              </div>
            </div>

            {/* The Graph Area */}
            <div className="flex-1 border border-zinc-800 rounded-xl bg-[#121215] flex flex-col p-5 shadow-inner relative min-h-0 min-w-0">
               {result && result.shapChartData && (
                 <h3 className="text-center text-xs font-bold tracking-widest uppercase text-zinc-300 mb-6">Probability Impact vs Hyperplane</h3>
               )}
               
               {result && result.shapChartData ? (
                <>
                  <style>{`
                    @keyframes wipeRight {
                      0% { clip-path: inset(0 100% 0 0); }
                      100% { clip-path: inset(0 -10% 0 0); }
                    }
                    .animate-trace-area .recharts-area-area,
                    .animate-trace-area .recharts-area-curve,
                    .animate-trace-area .recharts-area-dots,
                    .animate-trace-area .recharts-custom-dot {
                      animation: wipeRight 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
                    }
                  `}</style>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart className="animate-trace-area" data={result.shapChartData} margin={{ top: 20, right: 20, left: -10, bottom: 20 }}>
                    <defs>
                      <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                        <stop offset={gradientOffset} stopColor="#4A1818" stopOpacity={0.8} /> {/* Red Top */}
                        <stop offset={gradientOffset} stopColor="#143A23" stopOpacity={0.8} /> {/* Green Bottom */}
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
                    <XAxis 
                      dataKey="parameter" 
                      tick={{fontSize: 9, fill: '#71717A'}} 
                      axisLine={{stroke: '#3F3F46'}} 
                      tickLine={false}
                      angle={-25} textAnchor="end" height={60} 
                    />
                    <YAxis 
                      tick={{fontSize: 10, fill: '#A1A1AA'}} 
                      axisLine={{stroke: '#3F3F46'}} 
                      tickLine={false}
                      tickCount={5}
                    />
                    <RechartsTooltip 
                      contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#3F3F46', color: '#fff', fontSize: '11px', borderRadius: '8px' }}
                      itemStyle={{ color: '#E4E4E7' }}
                      formatter={(value: any) => [`${value}`, 'impact']}
                    />
                    <ReferenceLine y={0} stroke="#3F3F46" strokeDasharray="4 4" strokeWidth={1.5} label={{ position: 'insideBottomLeft', value: 'Hyperplane (Baseline Risk)', fill: '#71717A', fontSize: 10, dy: 15 }} />
                    
                    <Area 
                      type="monotone" 
                      dataKey="impact" 
                      stroke="#FFFFFF" 
                      fill="url(#splitColor)"
                      strokeWidth={3}
                      isAnimationActive={false}
                      activeDot={{ r: 6, fill: '#FFF' }}
                      dot={(props: any) => {
                        const { cx, cy, payload } = props;
                        // Red if impact > 0 (pulling into default), green if < 0 (saving)
                        const isRed = payload.impact > 0;
                        const fill = isRed ? "#EF4444" : "#4ADE80";
                        return <circle className="recharts-custom-dot" cx={cx} cy={cy} r={4.5} fill={fill} stroke="none" key={`dot-${payload.parameter}`} />;
                      }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
                </>
              ) : (
                 <div className="w-full h-full flex flex-col items-center justify-center">
                   {loading ? (
                     <div className="text-[#3b82f6] text-sm font-bold tracking-widest uppercase animate-pulse">
                       Generating Risk Probability Curve...
                     </div>
                   ) : (
                     <div className="text-zinc-700 text-xs font-bold tracking-widest uppercase">
                       Awaiting Analysis
                     </div>
                   )}
                 </div>
              )}
            </div>

          </div>

          {/* RIGHT COLUMN: Parameter Bar / Suggestions (span 3/12) */}
          <div className="lg:col-span-3 flex flex-col gap-5 relative min-h-0 min-w-0">

            {/* Absolute Parameter Graph */}
            <div className="flex-1 border border-zinc-800 rounded-xl bg-[#121215] p-5 shadow-md flex flex-col min-h-0 min-w-0">
              <h3 className="text-center font-bold text-[10px] uppercase tracking-widest border-b border-zinc-800 pb-3 mb-4 text-zinc-300">Parameter Chart</h3>
              <div className="flex-1 w-full relative">
                {result && result.shapChartData ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={result.shapChartData} margin={{ top: 10, right: 0, left: -25, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="2 2" stroke="#262626" vertical={false}/>
                      <XAxis dataKey="parameter" tick={false} axisLine={{stroke: '#3F3F46'}} tickLine={false} height={10} />
                      <YAxis tick={{fontSize: 9, fill: '#71717A'}} axisLine={false} tickLine={false} />
                      <RechartsTooltip 
                        contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#3F3F46', color: '#fff', fontSize: '10px' }}
                        itemStyle={{ color: '#FFE500', fontWeight: 'bold' }}
                        cursor={{fill: '#1A1A1E'}}
                        formatter={(value: any) => [`${value}`, 'absImpact']}
                      />
                      <Bar dataKey="absImpact" radius={[2, 2, 0, 0]} maxBarSize={30} isAnimationActive={true} animationDuration={1500}>
                          {result.shapChartData.map((entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
                          ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-zinc-700 text-[9px] font-bold uppercase tracking-widest">No Model Res</div>
                )}
              </div>
            </div>

            {/* Suggestions / Output Box */}
            <div className="flex-[1.2] border border-zinc-800 rounded-xl bg-[#121215] p-5 shadow-md flex flex-col overflow-hidden min-h-0 min-w-0">
              <h3 className="font-bold text-[10px] uppercase mb-4 border-b border-zinc-800 pb-3 text-zinc-300 tracking-widest shrink-0">
                Suggestions / Summary
              </h3>
              
              <div className="flex-1 overflow-y-auto pr-2 mt-1 text-xs">
                {!result && (
                  <div className="text-zinc-700 text-[10px] uppercase tracking-widest text-center mt-10">
                    Actionable insights will appear here
                  </div>
                )}

                {result && result.decision === 'APPROVED' && result.kfs && (
                  <div className="space-y-4">
                    <div className="text-[#4ADE80] mb-4 text-[10px] tracking-wide relative pl-3 uppercase">
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1 bg-[#4ADE80] rounded-full"></span>
                      Pre-Approved Loan Details
                    </div>
                    
                    <div className="flex border-b border-zinc-800/50 pb-2 justify-between items-center text-zinc-300 text-[11px] uppercase tracking-wide">
                      <span className="text-zinc-500">Int. Rate</span> 
                      <span>{result.kfs.interest_rate_pa}%</span>
                    </div>
                    <div className="flex border-b border-zinc-800/50 pb-2 justify-between items-center text-zinc-300 text-[11px] uppercase tracking-wide">
                      <span className="text-zinc-500">APR</span> 
                      <span>{result.kfs.apr}%</span>
                    </div>
                    <div className="flex border-b border-zinc-800/50 pb-2 justify-between items-center text-zinc-300 text-[11px] uppercase tracking-wide hidden">
                      <span className="text-zinc-500">Repayment</span> 
                      <span>₹{result.kfs.total_repayment}</span>
                    </div>
                    
                    <div className="flex justify-between items-center pt-2 text-[11px] text-zinc-300 uppercase tracking-wide">
                      <span className="text-[#4ADE80]">Monthly EMI</span> 
                      <span className="text-sm font-bold tracking-widest text-[#4ADE80]">₹{result.kfs.monthly_emi}</span>
                    </div>
                  </div>
                )}

                {result && result.decision === 'REJECTED' && result.reasons && (
                  <div className="space-y-3">
                    <div className="text-[#EF4444] mb-3 text-[10px] tracking-wide relative pl-3 uppercase">
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1 bg-[#EF4444] rounded-full"></span>
                      Primary Rejection Reasons
                    </div>
                    <ul className="space-y-3 font-medium text-zinc-300 text-[11px] border border-zinc-800 bg-[#16161A] p-4 rounded-lg">
                      {result.reasons.map((r: string, i: number) => (
                        <li key={i} className="flex gap-2">
                          <span className="text-zinc-600">-</span>
                          <span>{r}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {result && result.decision === 'REJECTED' && result.paths_to_approval && result.paths_to_approval.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-zinc-800 border-dashed">
                    <div className="text-[#F59E0B] mb-3 text-[10px] tracking-wide relative pl-3 uppercase">
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1 bg-[#F59E0B] rounded-full"></span>
                      Counterfactual Options
                    </div>
                    <div className="space-y-3">
                      {result.paths_to_approval.map((path: any, i: number) => (
                        <div key={i} className="bg-[#16161A] rounded p-3 text-[10px] border border-zinc-800/50">
                          <div className="text-zinc-500 uppercase tracking-widest mb-2 border-b border-zinc-800/50 pb-1">Path {i + 1}</div>
                          <ul className="space-y-2 mt-2 text-zinc-300">
                          {Object.keys(path).map(key => {
                              if (path[key] && path[key].advice) {
                                  return (
                                    <li key={key} className="flex gap-2 leading-relaxed">
                                      <span className="text-zinc-600">→</span>
                                      {path[key].advice}
                                    </li>
                                  )
                              }
                              return null;
                          })}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {result && (
                   <div className="mt-5 pt-4 border-t border-zinc-900 pb-2">
                     <button 
                       onClick={() => setShowJson(true)}
                       className="w-full border border-zinc-800 bg-[#16161A] hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100 rounded py-2 text-[9px] uppercase tracking-widest transition-colors cursor-pointer"
                     >
                       View Raw API Response
                     </button>
                   </div>
                )}
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* JSON Overlay Modal */}
      {showJson && result && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-[#121215] border border-zinc-800 rounded-xl w-full max-w-3xl flex flex-col max-h-[85vh] shadow-2xl">
            <div className="flex justify-between items-center p-4 border-b border-zinc-800 shrink-0">
              <h3 className="text-zinc-100 font-bold uppercase tracking-widest text-xs">Detailed Engine JSON Response</h3>
              <button onClick={() => setShowJson(false)} className="text-zinc-500 hover:text-zinc-100 text-2xl leading-none cursor-pointer">&times;</button>
            </div>
            <div className="p-4 overflow-y-auto flex-1 font-mono text-[10px] text-[#06b6d4]">
              <pre className="whitespace-pre-wrap word-break">{JSON.stringify(result, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
