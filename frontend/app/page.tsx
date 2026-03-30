"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, ReferenceLine, 
  ResponsiveContainer, BarChart, Bar, Cell 
} from "recharts";
import { ArrowRight, Activity, ShieldCheck, Database, FileText, Wifi, Check, Server, Lock } from "lucide-react";

export default function LandingPage() {
  // Sample data for visualizations
  const mockCurveData = [
    { name: "0s", val: -10 },
    { name: "1s", val: 5 },
    { name: "2s", val: 15 },
    { name: "3s", val: -5 },
    { name: "4s", val: 25 },
    { name: "5s", val: 35 },
    { name: "6s", val: 40 },
    { name: "7s", val: 20 },
    { name: "8s", val: 55 },
    { name: "9s", val: 75 },
    { name: "10s", val: 85 }
  ];

  const featureImpactData = [
    { parameter: "income_proxy", impact: 0.15, absImpact: 0.15 },
    { parameter: "stability_index", impact: 0.12, absImpact: 0.12 },
    { parameter: "affordability_index", impact: 0.08, absImpact: 0.08 },
    { parameter: "nsf_frequency", impact: -0.18, absImpact: 0.18 },
    { parameter: "network_centrality", impact: 0.05, absImpact: 0.05 },
    { parameter: "bill_latency", impact: -0.10, absImpact: 0.10 },
    { parameter: "digital_intensity", impact: 0.07, absImpact: 0.07 }
  ];

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-zinc-100 font-mono selection:bg-zinc-800">
      
      {/* Navigation Layer */}
      <nav className="fixed top-0 w-full z-50 border-b border-zinc-800/80 bg-[#0d0d0d]/90 backdrop-blur-md px-6 py-4 flex justify-between items-center">
        <div className="text-sm md:text-base font-bold uppercase tracking-widest text-zinc-100 flex items-center gap-2">
          <div className="w-2 h-2 bg-[#4ADE80] rounded-sm"></div>
          ECR Engine
        </div>
        <div className="flex gap-4">
          <Link href="/dashboard" className="px-4 py-2 border border-zinc-700 bg-[#16161A] hover:bg-zinc-800 text-[10px] md:text-xs font-bold uppercase tracking-widest transition-colors rounded text-zinc-300">
            Engine UI
          </Link>
        </div>
      </nav>

      <main className="pt-24 pb-20 px-4 md:px-8 max-w-[1400px] mx-auto flex flex-col gap-24 relative z-10">

        {/* 1. Hero Section with Background Image */}
        <section className="min-h-[75vh] grid lg:grid-cols-12 gap-10 items-center relative py-12 lg:py-0">
          {/* Background Image Accent Component */}
          <div className="absolute inset-0 z-0 overflow-hidden rounded-[2.5rem] pointer-events-none">
            <div className="absolute w-[800px] h-[800px] -top-32 -left-64 opacity-[0.15] mix-blend-screen overflow-hidden">
               <Image 
                 src="/bg-hero.png" 
                 alt="Fintech nodes background" 
                 fill 
                 className="object-cover animate-pulse mix-blend-hard-light" 
                 style={{ animationDuration: "8s" }} 
                 unoptimized 
               />
               <div className="absolute inset-0 bg-gradient-to-r from-[#0d0d0d] via-transparent to-[#0d0d0d]" />
               <div className="absolute inset-0 bg-gradient-to-b from-[#0d0d0d] via-transparent to-[#0d0d0d]" />
            </div>
          </div>

          <div className="lg:col-span-6 flex flex-col gap-6 relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 border border-zinc-800 bg-[#16161A]/80 backdrop-blur-sm rounded text-[10px] uppercase font-bold tracking-widest text-[#06b6d4] w-fit shadow-md">
              <Activity className="w-3 h-3" /> System Operational
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold uppercase tracking-tighter leading-[1.1] text-zinc-100">
              Explainable <br />
              <span className="text-[#4ADE80]">Credit Risk Engine </span> <br />
              For India
            </h1>
            <p className="text-sm md:text-base text-zinc-400 max-w-lg leading-relaxed border-l-2 border-zinc-800 pl-4 py-1">
              Alternative-data lending for thin-file borrowers with SHAP explainability and RBI-compliant decision transparency.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 mt-4">
              <Link href="/dashboard" className="h-12 px-6 bg-zinc-100 hover:bg-white text-black text-xs font-bold uppercase tracking-widest flex items-center justify-center gap-2 rounded transition-transform active:scale-95">
                View Explainability Engine <ArrowRight className="w-4 h-4" />
              </Link>
              <a href="#architecture" className="h-12 px-6 border border-zinc-700 hover:border-zinc-500 bg-[#121215]/80 backdrop-blur-sm text-zinc-300 text-xs font-bold uppercase tracking-widest flex items-center justify-center rounded transition-colors">
                Explore Architecture
              </a>
            </div>
          </div>
          
          <div className="lg:col-span-6 h-[400px] border border-zinc-800 bg-[#121215]/80 backdrop-blur-sm rounded-xl p-6 shadow-2xl relative overflow-hidden flex flex-col z-10 transition-transform duration-500 hover:scale-[1.02]">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#0d0d0d]/40 pointer-events-none z-10" />
            <div className="flex justify-between items-center border-b border-zinc-800 pb-4 mb-4 z-20 shrink-0">
              <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-widest">Live Model Inference</span>
              <span className="text-[10px] uppercase font-bold text-[#4ADE80] tracking-widest flex items-center gap-2">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#4ADE80] opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-[#4ADE80]"></span>
                </span>
                Processing
              </span>
            </div>
            {/* pointer-events-none ensures you can scroll even while your mouse is over the chart */}
            <div className="flex-1 w-full relative z-20 min-h-0 pointer-events-none">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockCurveData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="heroGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#4ADE80" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="#4ADE80" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
                  <XAxis dataKey="name" tick={{fontSize: 9, fill: '#71717A'}} axisLine={{stroke: '#3F3F46'}} tickLine={false} />
                  <YAxis tick={{fontSize: 9, fill: '#71717A'}} axisLine={{stroke: '#3F3F46'}} tickLine={false} />
                  <ReferenceLine y={0} stroke="#3F3F46" strokeDasharray="4 4" />
                  <Area className="animate-in fade-in slide-in-from-left-8 duration-1000" type="monotone" dataKey="val" stroke="#4ADE80" fill="url(#heroGradient)" strokeWidth={2} isAnimationActive={false} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* 2. Features Strategy Section */}
        <section className="border-y border-zinc-800 py-16 bg-[#121215]/30 relative">
          <div className="absolute top-0 right-10 w-96 h-96 bg-[#06b6d4]/5 rounded-full blur-3xl pointer-events-none" />
          <div className="text-center mb-10 relative z-10">
            <h2 className="text-xl font-bold uppercase tracking-widest text-[#06b6d4]">Alternative Data Extractor</h2>
            <p className="text-xs text-zinc-500 mt-2 font-mono">Assessing capability over history</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 divide-y md:divide-y-0 md:divide-x divide-zinc-800 relative z-10">
            <div className="flex flex-col p-4">
              <div className="text-sm font-bold text-zinc-100 mb-2 uppercase tracking-wide">UPI Transactions</div>
              <div className="text-[11px] text-zinc-400 mb-2">Income Proxy, Cluster Consistency, Savings Buffer</div>
              <div className="text-[10px] uppercase tracking-widest text-[#4ADE80] mt-auto pt-4">Direct behavior signal</div>
            </div>
            <div className="flex flex-col p-4">
              <div className="text-sm font-bold text-zinc-100 mb-2 uppercase tracking-wide">Network Centrality</div>
              <div className="text-[11px] text-zinc-400 mb-2">Eigenvector Centrality across trusted merchant nodes</div>
              <div className="text-[10px] uppercase tracking-widest text-[#4ADE80] mt-auto pt-4">Social Proof</div>
            </div>
            <div className="flex flex-col p-4">
              <div className="text-sm font-bold text-zinc-100 mb-2 uppercase tracking-wide">SMS Parsing</div>
              <div className="text-[11px] text-zinc-400 mb-2">ADB, Cash Flow Stress (NSF Frequency), Time-to-Zero</div>
              <div className="text-[10px] uppercase tracking-widest text-[#4ADE80] mt-auto pt-4">Virtual Ledger</div>
            </div>
            <div className="flex flex-col p-4">
              <div className="text-sm font-bold text-zinc-100 mb-2 uppercase tracking-wide">Affordability Index</div>
              <div className="text-[11px] text-zinc-400 mb-2">Income vs Rent/Utility/EMI ratio, Bill Latency</div>
              <div className="text-[10px] uppercase tracking-widest text-[#4ADE80] mt-auto pt-4">Willingness to pay</div>
            </div>
          </div>
        </section>

        {/* 3. Four-Pillar Architecture Grid */}
        <section id="architecture" className="pt-10 hover:opacity-100">
          <div className="flex items-center gap-4 mb-10 border-b border-zinc-800 pb-4">
            <h2 className="text-sm font-bold uppercase tracking-widest text-zinc-300">Architecture Grid</h2>
            <div className="flex-1 h-[1px] bg-zinc-800"></div>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            <div className="group border border-zinc-800 bg-[#121215] p-6 rounded-xl hover:bg-[#16161A] hover:border-[#3b82f6] transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#3b82f6]/10 rounded-bl-full translate-x-10 -translate-y-10 group-hover:bg-[#3b82f6]/20 transition-colors pointer-events-none"></div>
              <div className="relative z-10 pointer-events-none">
                <Database className="w-8 h-8 text-[#3b82f6] mb-4 drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]" />
                <h3 className="text-sm font-bold uppercase tracking-wide text-zinc-100 mb-2 group-hover:text-white">Alternative Data Intelligence</h3>
              </div>
              <p className="text-[11px] text-zinc-500 leading-relaxed font-mono relative z-10 pointer-events-none">Processes localized datasets including utility payments, digital footprints, and geospatial risk mapping.</p>
            </div>

            <div className="group border border-zinc-800 bg-[#121215] p-6 rounded-xl hover:bg-[#16161A] hover:border-[#eab308] transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#eab308]/10 rounded-bl-full translate-x-10 -translate-y-10 group-hover:bg-[#eab308]/20 transition-colors pointer-events-none"></div>
              <div className="relative z-10 pointer-events-none">
                <Server className="w-8 h-8 text-[#eab308] mb-4 drop-shadow-[0_0_8px_rgba(234,179,8,0.5)]" />
                <h3 className="text-sm font-bold uppercase tracking-wide text-zinc-100 mb-2 group-hover:text-white">Fair LightGBM Models</h3>
              </div>
              <p className="text-[11px] text-zinc-500 leading-relaxed font-mono relative z-10 pointer-events-none">Gradient boosting machines calibrated for monotonic constraints to prevent algorithmic bias.</p>
            </div>

            <div className="group border border-zinc-800 bg-[#121215] p-6 rounded-xl hover:bg-[#16161A] hover:border-[#a855f7] transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#a855f7]/10 rounded-bl-full translate-x-10 -translate-y-10 group-hover:bg-[#a855f7]/20 transition-colors pointer-events-none"></div>
              <div className="relative z-10 pointer-events-none">
                <Activity className="w-8 h-8 text-[#a855f7] mb-4 drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]" />
                <h3 className="text-sm font-bold uppercase tracking-wide text-zinc-100 mb-2 group-hover:text-white">SHAP Explainability</h3>
              </div>
              <p className="text-[11px] text-zinc-500 leading-relaxed font-mono relative z-10 pointer-events-none">Game-theoretic contribution mapping translating complex predictions into actionable reason codes.</p>
            </div>

            <div className="group border border-zinc-800 bg-[#121215] p-6 rounded-xl hover:bg-[#16161A] hover:border-[#4ADE80] transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#4ADE80]/10 rounded-bl-full translate-x-10 -translate-y-10 group-hover:bg-[#4ADE80]/20 transition-colors pointer-events-none"></div>
              <div className="relative z-10 pointer-events-none">
                <ShieldCheck className="w-8 h-8 text-[#4ADE80] mb-4 drop-shadow-[0_0_8px_rgba(74,222,128,0.5)]" />
                <h3 className="text-sm font-bold uppercase tracking-wide text-zinc-100 mb-2 group-hover:text-white">RBI & DPDP Compliance</h3>
              </div>
              <p className="text-[11px] text-zinc-500 leading-relaxed font-mono relative z-10 pointer-events-none">Strict data localization, immutable audit trails, and privacy-preserving inference pipelines.</p>
            </div>
          </div>
        </section>

        {/* 4. Feature Intelligence Panel & 5. Explainability Section */}
        <section className="pt-10 grid lg:grid-cols-12 gap-6 relative">
          
          <div className="lg:col-span-4 flex flex-col gap-6">
            <div className="border border-zinc-800 bg-[#121215] p-5 rounded-xl flex flex-col h-full shadow-md z-10 hover:border-zinc-700 transition-colors">
              <h3 className="text-[10px] font-bold uppercase tracking-widest text-zinc-300 border-b border-zinc-800 pb-3 mb-4 flex items-center gap-2">
                <FileText className="w-3 h-3 text-[#f59e0b]" /> Feature Extraction Vector
              </h3>
              <ul className="space-y-3 mt-2 pointer-events-none">
                {featureImpactData.map((feat, i) => (
                  <li key={i} className="flex justify-between items-center text-xs p-2 bg-[#16161A] border border-zinc-800/50 rounded">
                    <span className="text-zinc-400 font-mono">{feat.parameter}</span>
                    <span className={`font-mono text-[10px] ${feat.impact > 0 ? "text-[#4ADE80] drop-shadow-[0_0_4px_rgba(74,222,128,0.5)]" : "text-[#EF4444] drop-shadow-[0_0_4px_rgba(239,68,68,0.5)]"}`}>
                      {feat.impact > 0 ? "+" : ""}{feat.impact}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="lg:col-span-8 border border-zinc-800 bg-[#121215] p-5 rounded-xl shadow-[0_4px_30px_rgba(0,0,0,0.5)] min-h-[400px] flex flex-col z-10">
            <h3 className="text-[10px] font-bold uppercase tracking-widest text-zinc-300 border-b border-zinc-800 pb-3 mb-4 flex justify-between items-center">
              <span>Explainability Waterfall Analysis</span>
              <span className="text-zinc-500 border border-zinc-800 bg-[#16161A] px-2 py-0.5 rounded text-[9px]">SHAP Vector Space</span>
            </h3>
            
            <div className="flex-1 w-full mt-4 pointer-events-none">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featureImpactData} layout="vertical" margin={{ top: 0, right: 30, left: 40, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="2 2" stroke="#262626" horizontal={true} vertical={false}/>
                  <XAxis type="number" tick={{fontSize: 9, fill: '#71717A'}} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="parameter" tick={{fontSize: 9, fill: '#A1A1AA'}} axisLine={{stroke: '#3F3F46'}} tickLine={false} width={120} />
                  <Bar dataKey="impact" barSize={16} radius={2} isAnimationActive={false}>
                      {featureImpactData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#4ADE80' : '#EF4444'} />
                      ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-6 pt-4 border-t border-zinc-800/50 grid grid-cols-2 gap-4">
               <div className="bg-[#16161A] p-3 rounded border border-zinc-800/50">
                  <div className="text-[9px] uppercase font-bold text-zinc-500 tracking-widest mb-1">Base Score</div>
                  <div className="text-2xl font-bold text-zinc-400">420</div>
               </div>
               <div className="bg-[#16161A] p-3 rounded border border-zinc-800 border-l-2 border-l-[#4ADE80]">
                  <div className="text-[9px] uppercase font-bold text-[#4ADE80] tracking-widest mb-1 drop-shadow-[0_0_2px_rgba(74,222,128,0.5)]">Final Probability</div>
                  <div className="text-2xl font-bold text-zinc-100">83.5% <span className="text-xs text-[#4ADE80] uppercase tracking-wide align-middle ml-2">Approved</span></div>
               </div>
            </div>
            
            <div className="mt-4 border border-zinc-800/80 px-4 py-3 bg-[#0d0d0d] rounded-lg">
              <div className="text-[#F59E0B] mb-2 text-[10px] tracking-wide relative pl-3 uppercase font-bold drop-shadow-[0_0_2px_rgba(245,158,11,0.5)]">
                <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-[#F59E0B] rounded-full animate-pulse"></span>
                Example Counterfactual (Paths to Approval)
              </div>
              <div className="text-[11px] text-zinc-400 flex items-center gap-3">
                <ArrowRight className="w-3 h-3 text-zinc-600" /> Reduce `bill_latency` by 2 days to cross 85% probability threshold.
              </div>
            </div>
          </div>
        </section>

        {/* 6. Compliance & 7. Offline Architecture */}
        <section className="pt-10 grid md:grid-cols-2 gap-6 relative">
          
          {/* Subtle Right Side Background Image Overlay on this card */}
          <div className="border border-zinc-800 bg-[#121215] p-6 rounded-xl relative overflow-hidden group hover:border-[#06b6d4] transition-colors">
             <div className="absolute right-0 top-0 w-64 h-full pointer-events-none opacity-20 group-hover:opacity-40 transition-opacity mix-blend-screen overflow-hidden">
               <Image 
                 src="/bg-hero.png" 
                 alt="Fintech background" 
                 fill 
                 className="object-cover" 
                 unoptimized
                 style={{ mixBlendMode: 'color-dodge', transform: 'scale(1.2) translateX(20%)' }}
               />
               <div className="absolute inset-0 bg-gradient-to-r from-[#121215] to-transparent"></div>
             </div>
             
             <div className="absolute top-4 right-4 text-zinc-800"><Lock className="w-24 h-24 opacity-20" /></div>
             <h3 className="text-sm font-bold uppercase tracking-widest text-[#06b6d4] mb-6 relative z-10 drop-shadow-[0_0_8px_rgba(6,182,212,0.4)]">Compliance Integrity</h3>
             <ul className="space-y-4 relative z-10 pointer-events-none">
               <li className="flex gap-3">
                 <div className="mt-0.5"><Check className="w-4 h-4 text-[#06b6d4]" /></div>
                 <div>
                   <div className="text-xs font-bold text-zinc-200 uppercase tracking-wider mb-1">Immutable Audit Trails</div>
                   <div className="text-[11px] text-zinc-500 font-mono">Every automated decision recorded for regulatory review.</div>
                 </div>
               </li>
               <li className="flex gap-3">
                 <div className="mt-0.5"><Check className="w-4 h-4 text-[#06b6d4]" /></div>
                 <div>
                   <div className="text-xs font-bold text-zinc-200 uppercase tracking-wider mb-1">Data Localization</div>
                   <div className="text-[11px] text-zinc-500 font-mono">100% processing confined to India-based VPCs.</div>
                 </div>
               </li>
               <li className="flex gap-3">
                 <div className="mt-0.5"><Check className="w-4 h-4 text-[#06b6d4]" /></div>
                 <div>
                   <div className="text-xs font-bold text-zinc-200 uppercase tracking-wider mb-1">Consent Ledger</div>
                   <div className="text-[11px] text-zinc-500 font-mono">DPDP-compliant tracking of borrower data access.</div>
                 </div>
               </li>
             </ul>
          </div>

          <div className="border border-zinc-800 bg-[#121215] p-6 rounded-xl relative overflow-hidden flex flex-col hover:border-[#a855f7] transition-colors">
             <div className="absolute top-4 right-4 text-zinc-800"><Wifi className="w-24 h-24 opacity-20" /></div>
             <div className="flex justify-between items-start mb-6 relative z-10 pointer-events-none">
               <h3 className="text-sm font-bold uppercase tracking-widest text-[#a855f7] drop-shadow-[0_0_8px_rgba(168,85,247,0.4)]">Offline-First PWA</h3>
               <div className="text-[9px] uppercase tracking-widest bg-[#16161A] border border-zinc-800 px-2 py-1 rounded text-zinc-400 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 bg-[#EF4444] rounded-full animate-pulse shadow-[0_0_4px_#ef4444]"></span>
                  Offline Mode Active
               </div>
             </div>
             <div className="flex-1 bg-[#16161A] border border-zinc-800/80 rounded block font-mono text-[10px] text-zinc-400 p-4 relative z-10 space-y-3 pointer-events-none">
               <div className="flex justify-between border-b border-zinc-800/50 pb-2">
                 <span className="text-zinc-500">ServiceWorker State</span>
                 <span className="text-[#a855f7]">Activated / Intercepting</span>
               </div>
               <div className="flex justify-between border-b border-zinc-800/50 pb-2">
                 <span className="text-zinc-500">IndexedDB Storage</span>
                 <span className="text-zinc-300">SyncQueue (3 items pending)</span>
               </div>
               <div className="flex justify-between border-b border-zinc-800/50 pb-2">
                 <span className="text-zinc-500">Background Sync</span>
                 <span className="text-[#4ADE80]">Awaiting Connectivity...</span>
               </div>
               <div className="pt-2 text-zinc-600 italic">
                 // Ensures uninterrupted application onboarding in tier-3 environments.
               </div>
             </div>
          </div>
        </section>

        {/* 8. Final CTA */}
        <section className="border border-zinc-800 bg-[#121215]/80 backdrop-blur-sm rounded-2xl p-10 md:p-16 text-center my-10 relative overflow-hidden transition-all hover:bg-[#121215]">
          <div className="absolute inset-x-0 bottom-0 h-2 bg-gradient-to-r from-transparent via-[#4ADE80] to-transparent opacity-40 blur-sm mix-blend-screen" />
          
          <h2 className="text-2xl md:text-3xl font-bold uppercase tracking-widest text-zinc-100 mb-6 max-w-2xl mx-auto leading-relaxed">
            Transform <span className="text-zinc-500 line-through decoration-zinc-800 block md:inline mx-2">"No credit history"</span> 
            <br className="md:hidden" /> into <br className="hidden md:block" /> 
            <span className="text-[#4ADE80] drop-shadow-[0_0_8px_rgba(74,222,128,0.3)]">"Approved using transaction intelligence."</span>
          </h2>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10 relative z-10">
            <Link href="/dashboard" className="h-14 px-8 bg-zinc-100 hover:bg-white text-black text-sm font-bold uppercase tracking-widest flex items-center justify-center gap-2 rounded-full transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.1)]">
              Launch Simulator <ArrowRight className="w-5 h-5" />
            </Link>
            <a href="https://github.com/AayushBeura/ECR-Engine" target="_blank" rel="noopener noreferrer" className="h-14 px-8 border border-zinc-700 hover:border-zinc-500 bg-[#16161A] text-zinc-300 text-sm font-bold uppercase tracking-widest flex items-center justify-center gap-2 rounded-full transition-colors hover:text-white">
              View Model Stack
            </a>
          </div>
        </section>

      </main>
    </div>
  );
}
