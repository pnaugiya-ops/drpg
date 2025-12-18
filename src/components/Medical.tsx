import React, { useRef, useState } from 'react';
import { FileText, Plus, Pill, Calendar, Activity, Download, ArrowLeft, Clock, ShieldCheck, AlertTriangle, Phone, Brain, Utensils, Thermometer, BedDouble, Scissors } from 'lucide-react';
import { Button } from './CoreUI';
import { Report, VitalStat } from '../types';
import { analyzeReportImage } from '../services/geminiService';

export const ReportViewer: React.FC<{ reports: Report[], onBack: ()=>void, onAddReport: (r: Report)=>void, vitalStats: VitalStat[], onAddVital: (v: VitalStat)=>void }> = ({ reports, onBack, onAddReport, onAddVital }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setIsAnalyzing(true);
      try {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = async () => {
          const base64 = (reader.result as string).split(',')[1];
          const analysis = await analyzeReportImage(base64, file.type);
          const newReport: Report = {
            id: Date.now().toString(),
            patientId: 'p1',
            title: file.name,
            date: analysis.reportDate || new Date().toISOString().split('T')[0],
            type: 'Blood',
            summary: analysis.summary
          };
          if (analysis.hemoglobin) onAddVital({ date: newReport.date, value: analysis.hemoglobin, unit: 'g/dL', label: 'Hemoglobin' });
          onAddReport(newReport);
        };
      } finally { setIsAnalyzing(false); }
    }
  };

  return (
    <div className="space-y-6 animate-medical-in">
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
                <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-xl text-gray-600"><ArrowLeft className="w-5 h-5" /></button>
                <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Health History</h2>
            </div>
            <input type="file" ref={fileInputRef} className="hidden" onChange={handleFileUpload} accept="image/*" />
            <Button onClick={() => fileInputRef.current?.click()} size="sm">{isAnalyzing ? "AI Analyzing..." : <><Plus className="w-4 h-4 mr-2" /> Upload Report</>}</Button>
        </div>
        <div className="grid gap-4">
            {reports.map(r => (
                <div key={r.id} className="p-6 bg-white rounded-[2rem] border border-gray-100 shadow-sm flex items-center justify-between group hover:border-rose-200 transition-all">
                    <div className="flex items-center gap-4">
                        <div className="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center text-rose-500 group-hover:bg-rose-500 group-hover:text-white transition-colors"><FileText className="w-7 h-7" /></div>
                        <div>
                            <div className="font-bold text-gray-900 text-lg">{r.title}</div>
                            <div className="text-[10px] text-gray-400 font-black uppercase tracking-widest">{r.date} • {r.type}</div>
                            {r.summary && <p className="text-xs text-rose-600 font-bold mt-1 flex items-center gap-1"><Brain size={12}/> {r.summary}</p>}
                        </div>
                    </div>
                    <button className="p-3 text-gray-400 hover:text-rose-600 hover:bg-rose-50 rounded-2xl transition-all"><Download className="w-6 h-6" /></button>
                </div>
            ))}
        </div>
    </div>
  );
};

export const SurgeryGuide: React.FC<{ onBack: ()=>void }> = ({ onBack }) => {
    const [activeTab, setActiveTab] = useState<'pre-op' | 'post-op' | 'warning'>('pre-op');
    return (
        <div className="space-y-8 animate-medical-in pb-12">
            <div className="flex items-center gap-3">
                <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-xl text-gray-600"><ArrowLeft className="w-5 h-5" /></button>
                <h2 className="text-3xl font-black text-gray-900 italic tracking-tight uppercase">Surgery Center</h2>
            </div>
            <div className="bg-teal-600 p-10 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden">
                <div className="relative z-10">
                    <h3 className="text-2xl font-black mb-4 flex items-center gap-2"><Scissors /> Laparoscopic Specialist</h3>
                    <p className="text-teal-50 max-w-2xl text-lg font-medium opacity-90 leading-relaxed">Advanced keyhole surgery performed by Dr. Priyanka Gupta. This minimally invasive technique ensures 1-2 small incisions, significantly less pain, and a return to daily life within days.</p>
                </div>
                <Activity className="absolute -right-8 -top-8 w-48 h-48 opacity-10" />
            </div>
            <div className="flex gap-2 p-1 bg-gray-100 rounded-2xl w-fit">
                {['pre-op', 'post-op', 'warning'].map(tab => (
                    <button key={tab} onClick={() => setActiveTab(tab as any)} className={`px-6 py-3 rounded-xl font-bold text-sm transition-all ${activeTab === tab ? 'bg-white text-teal-600 shadow-sm' : 'text-gray-500'}`}>
                        {tab === 'pre-op' ? 'Pre-Op Preparation' : tab === 'post-op' ? 'Recovery Guide' : 'Warning Signs'}
                    </button>
                ))}
            </div>
            <div className="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-xl min-h-[300px]">
                {activeTab === 'pre-op' && (
                    <div className="grid md:grid-cols-2 gap-8 animate-in slide-in-from-bottom-2">
                        <div className="space-y-6">
                            <div className="flex gap-4"><div className="w-12 h-12 rounded-2xl bg-orange-100 text-orange-600 flex items-center justify-center font-black shrink-0">1</div><div><h4 className="font-bold text-gray-900">NPO Status (Fasting)</h4><p className="text-sm text-gray-500">Strictly no food or water for 8-10 hours before the surgery time to avoid anesthesia complications.</p></div></div>
                            <div className="flex gap-4"><div className="w-12 h-12 rounded-2xl bg-blue-100 text-blue-600 flex items-center justify-center font-black shrink-0">2</div><div><h4 className="font-bold text-gray-900">Bowel Preparation</h4><p className="text-sm text-gray-500">Follow the prescribed liquid diet/laxative instructions provided during your pre-op consult.</p></div></div>
                            <div className="flex gap-4"><div className="w-12 h-12 rounded-2xl bg-teal-100 text-teal-600 flex items-center justify-center font-black shrink-0">3</div><div><h4 className="font-bold text-gray-900">Clinic Essentials</h4><p className="text-sm text-gray-500">Carry your Aadhaar Card, previous ultrasound reports, and blood work files.</p></div></div>
                        </div>
                        <div className="bg-slate-50 p-8 rounded-[2rem] border border-slate-100">
                            <h4 className="font-bold text-gray-800 mb-4 uppercase text-xs tracking-widest">Day of Procedure</h4>
                            <ul className="space-y-3 text-sm text-gray-600 font-medium">
                                <li>• Shower with antiseptic soap</li>
                                <li>• Remove all jewelry, nail paint, and piercings</li>
                                <li>• Wear comfortable, loose front-opening clothes</li>
                                <li>• Arrive 2 hours prior to scheduled time</li>
                            </ul>
                        </div>
                    </div>
                )}
                {activeTab === 'post-op' && (
                    <div className="grid md:grid-cols-3 gap-6 animate-in slide-in-from-bottom-2">
                         <div className="bg-blue-50 p-6 rounded-[2rem] border border-blue-100"><BedDouble className="w-10 h-10 text-blue-600 mb-4"/><h4 className="font-bold text-blue-900 mb-2">Immediate Rest</h4><p className="text-xs text-blue-800 font-medium leading-relaxed">Walk gently inside your room from evening of surgery. Avoid heavy lifting for 2 weeks.</p></div>
                         <div className="bg-orange-50 p-6 rounded-[2rem] border border-orange-100"><Utensils className="w-10 h-10 text-orange-600 mb-4"/><h4 className="font-bold text-orange-900 mb-2">Nutrition</h4><p className="text-xs text-orange-800 font-medium leading-relaxed">Start with clear liquids (coconut water/tea). Progress to semi-solids as per nurse instructions.</p></div>
                         <div className="bg-teal-50 p-6 rounded-[2rem] border border-teal-100"><ShieldCheck className="w-10 h-10 text-teal-600 mb-4"/><h4 className="font-bold text-teal-900 mb-2">Wound Care</h4><p className="text-xs text-teal-800 font-medium leading-relaxed">Keep the keyhole dressing dry. You can sponge bathe. Do not apply any creams locally.</p></div>
                    </div>
                )}
                {activeTab === 'warning' && (
                    <div className="bg-red-50 p-10 rounded-[2.5rem] border border-red-100 animate-in zoom-in-95">
                        <h4 className="text-2xl font-black text-red-900 flex items-center gap-3 mb-6"><AlertTriangle /> Emergency Indicators</h4>
                        <div className="grid md:grid-cols-2 gap-4 text-red-800 font-bold">
                            <div className="bg-white p-5 rounded-xl shadow-sm flex items-center gap-3 border border-red-100"><Thermometer size={18}/> Fever exceeding 100.4°F</div>
                            <div className="bg-white p-5 rounded-xl shadow-sm flex items-center gap-3 border border-red-100"><AlertTriangle size={18}/> Severe abdominal distension/pain</div>
                            <div className="bg-white p-5 rounded-xl shadow-sm flex items-center gap-3 border border-red-100"><Activity size={18}/> Excessive redness at incision sites</div>
                            <div className="bg-white p-5 rounded-xl shadow-sm flex items-center gap-3 border border-red-100"><Phone size={18}/> Uncontrolled nausea/vomiting</div>
                        </div>
                    </div>
                )}
            </div>
            <div className="bg-indigo-900 p-8 rounded-[2.5rem] text-white flex flex-col md:flex-row justify-between items-center gap-6 shadow-2xl">
                 <div className="flex items-center gap-6"><div className="bg-white/10 p-5 rounded-2xl"><Phone className="w-8 h-8" /></div><div><h4 className="font-bold text-xl">Surgical Emergency Hotline</h4><p className="text-indigo-200 font-medium">Priority line for post-operative patients of Dr. Priyanka Gupta.</p></div></div>
                 <Button onClick={() => window.open('tel:+919676712517')} className="bg-white text-indigo-900 border-0 px-10 font-black">Call +91 96767 12517</Button>
            </div>
        </div>
    );
};

export const Pharmacy: React.FC = () => (
    <div className="space-y-6 animate-medical-in">
        <div className="bg-gradient-to-br from-emerald-600 to-teal-700 p-10 rounded-[2.5rem] text-white shadow-xl flex justify-between items-center overflow-hidden relative">
            <div className="relative z-10"><h2 className="text-3xl font-black mb-2 italic tracking-tight uppercase">Bhavya Pharmacy</h2><p className="opacity-90 max-w-md font-medium">In-house specialized gynecological medicines and infertility supplements.</p></div>
            <Pill className="w-32 h-32 opacity-10 absolute -right-4 -bottom-4 rotate-12" />
        </div>
        <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm min-h-[250px] flex flex-col justify-center items-center text-center">
                <Clock className="w-10 h-10 text-emerald-100 mb-4" /><h3 className="font-bold text-gray-900 text-xl">Prescriptions</h3><p className="text-gray-400 text-sm font-medium mt-2">No active refills found.</p>
            </div>
            <div className="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm min-h-[250px] flex flex-col justify-center items-center text-center">
                <FileText className="w-10 h-10 text-gray-100 mb-4" /><h3 className="font-bold text-gray-900 text-xl">Medication Logs</h3><p className="text-gray-400 text-sm font-medium mt-2">Your history will appear here.</p>
            </div>
        </div>
    </div>
);

export const AppointmentBooking: React.FC<{ onBack: ()=>void }> = ({ onBack }) => (
    <div className="max-w-2xl mx-auto space-y-6 animate-medical-in">
        <div className="flex items-center gap-3">
            <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-xl text-gray-600"><ArrowLeft className="w-5 h-5" /></button>
            <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Request Visit</h2>
        </div>
        <div className="bg-white p-10 rounded-[2.5rem] border border-gray-100 shadow-2xl space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3"><label className="text-[10px] font-black text-gray-300 uppercase tracking-widest ml-1">Preferred Date</label><input type="date" className="w-full p-5 bg-slate-50 rounded-2xl border-0 focus:ring-4 focus:ring-rose-500/10 font-bold" /></div>
                <div className="space-y-3"><label className="text-[10px] font-black text-gray-300 uppercase tracking-widest ml-1">Preferred Time</label><select className="w-full p-5 bg-slate-50 rounded-2xl border-0 font-bold appearance-none"><option>Morning (11AM-2PM)</option><option>Evening (6PM-8PM)</option></select></div>
            </div>
            <Button fullWidth size="lg" className="py-6 text-base rounded-[1.5rem]">Send Request</Button>
            <p className="text-center text-[10px] text-gray-400 font-bold uppercase tracking-tighter">Dr. Gupta's team will confirm via WhatsApp shortly.</p>
        </div>
    </div>
);