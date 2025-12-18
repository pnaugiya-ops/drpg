import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Stethoscope, Loader2, ArrowLeft, RefreshCw, HelpCircle, ChevronDown, AlertTriangle } from 'lucide-react';
import { sendMessageToGemini, resetSymptomSession } from '../services/geminiService';
import { ChatMessage } from '../types';
import { FAQS } from '../constants';

export const ChatInterface: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([{ id: '1', role: 'model', text: "Hello! I'm Dr. Gupta's AI assistant. How can I help you with your women's health concerns today?", timestamp: Date.now() }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => { scrollRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg: ChatMessage = { id: Date.now().toString(), role: 'user', text: input, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    const modelMsgId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, { id: modelMsgId, role: 'model', text: '', timestamp: Date.now() }]);
    let fullRes = '';
    try { await sendMessageToGemini(input, (chunk) => { fullRes += chunk; setMessages(prev => prev.map(m => m.id === modelMsgId ? { ...m, text: fullRes } : m)); }); } 
    catch (e) { setMessages(prev => prev.map(m => m.id === modelMsgId ? { ...m, text: "Connectivity issue. Try again." } : m)); } 
    finally { setIsLoading(false); }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-white rounded-[2.5rem] shadow-2xl border border-gray-100 overflow-hidden animate-medical-in">
      <div className="p-6 border-b bg-rose-50/30 flex items-center justify-between">
        <div className="flex items-center gap-4"><button onClick={onBack} className="p-2 hover:bg-white rounded-xl text-rose-600"><ArrowLeft className="w-5 h-5" /></button><div><h3 className="font-black text-gray-900 tracking-tight">AI Concierge</h3><p className="text-[10px] text-rose-500 font-black uppercase tracking-widest">Medical Assistant</p></div></div><Bot className="text-rose-600 w-6 h-6" />
      </div>
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50 scrollbar-hide">
        {messages.map(m => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] p-5 rounded-[2rem] shadow-sm ${m.role === 'user' ? 'bg-rose-600 text-white rounded-tr-none' : 'bg-white border text-gray-800 rounded-tl-none font-medium text-sm'}`}>
              <p className="whitespace-pre-wrap">{m.text}</p>
            </div>
          </div>
        ))}
        {isLoading && !messages[messages.length-1].text && (<div className="flex justify-start"><div className="bg-white border p-5 rounded-[1.5rem] flex items-center gap-3 text-gray-400"><Loader2 className="w-4 h-4 animate-spin text-rose-500" /><span className="text-xs font-bold uppercase">Consulting AI...</span></div></div>)}
        <div ref={scrollRef} />
      </div>
      <div className="p-4 bg-white border-t flex gap-2"><input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} className="flex-1 px-6 py-4 border-0 bg-gray-100 rounded-2xl focus:ring-4 focus:ring-rose-500/10 outline-none text-sm font-semibold" placeholder="Ask about wellness or care..." /><button onClick={handleSend} disabled={isLoading} className="p-4 bg-rose-600 text-white rounded-2xl hover:bg-rose-700 transition-all shadow-lg shadow-rose-100"><Send className="w-5 h-5" /></button></div>
    </div>
  );
};

export const SymptomChecker: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([{ id: '1', role: 'model', text: "Welcome to Dr. Gupta's Symptom Triage. Describe your concern clearly (e.g. 'lower abdominal pain').", timestamp: Date.now() }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg: ChatMessage = { id: Date.now().toString(), role: 'user', text: input, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    let fullRes = '';
    const modelId = Date.now().toString();
    setMessages(prev => [...prev, { id: modelId, role: 'model', text: '', timestamp: Date.now() }]);
    try { await sendMessageToGemini(input, (chunk) => { fullRes += chunk; setMessages(prev => prev.map(m => m.id === modelId ? { ...m, text: fullRes } : m)); }, 'symptom'); } finally { setIsLoading(false); }
  };
  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-white rounded-[2.5rem] shadow-2xl border border-gray-100 overflow-hidden animate-medical-in">
      <div className="bg-teal-600 text-white p-6 flex items-center justify-between"><div className="flex items-center gap-3"><Stethoscope className="w-6 h-6" /><h3 className="font-bold text-lg">AI Symptom Triage</h3></div><button onClick={() => { resetSymptomSession(); window.location.reload(); }} className="p-2 hover:bg-white/10 rounded-xl"><RefreshCw size={18}/></button></div>
      <div className="bg-amber-50 p-4 border-b flex gap-3 text-xs text-amber-800 font-bold"><AlertTriangle className="w-5 h-5 shrink-0" /><p>Not for emergencies. If you have heavy bleeding or severe pain, visit the nearest ER immediately.</p></div>
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">{messages.map(m => (<div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}><div className={`max-w-[85%] p-5 rounded-[2rem] shadow-sm ${m.role === 'user' ? 'bg-teal-600 text-white rounded-tr-none' : 'bg-white border text-gray-800 font-medium text-sm'}`}><p className="whitespace-pre-wrap">{m.text}</p></div></div>))}</div>
      <div className="p-4 bg-white border-t flex gap-2"><input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} className="flex-1 px-6 py-4 bg-gray-100 border-0 rounded-2xl outline-none text-sm font-semibold" placeholder="Describe symptoms..." /><button onClick={handleSend} className="p-4 bg-teal-600 text-white rounded-2xl shadow-lg transition-all"><Send className="w-5 h-5" /></button></div>
    </div>
  );
};

export const FAQSection: React.FC = () => {
  const [openId, setOpenId] = useState<string | null>(null);
  const categories = Array.from(new Set(FAQS.map(f => f.category))) as string[];
  return (
    <div className="max-w-3xl mx-auto space-y-10 py-6 animate-medical-in">
      <div className="text-center mb-12"><div className="inline-flex p-4 bg-rose-100 rounded-[1.5rem] text-rose-600 mb-6 shadow-sm"><HelpCircle className="w-10 h-10" /></div><h2 className="text-3xl font-black text-gray-900 tracking-tight italic">Health Insights</h2><p className="text-gray-500 mt-2 font-medium">Specialist knowledge at your fingertips.</p></div>
      <div className="space-y-12">{categories.map(category => (<div key={category} className="space-y-4"><h3 className="text-[10px] font-black text-rose-600 uppercase tracking-[0.3em] ml-2">{category}</h3><div className="space-y-3">{FAQS.filter(f => f.category === category).map((faq) => { const isOpen = openId === faq.id; return (<div key={faq.id} className="bg-white rounded-[1.5rem] border border-gray-100 shadow-sm overflow-hidden hover:shadow-md transition-all"><button onClick={() => setOpenId(isOpen ? null : faq.id)} className="w-full flex items-center justify-between p-6 text-left focus:outline-none group"><span className="font-bold text-gray-800 group-hover:text-rose-600 transition-colors leading-tight">{faq.question}</span><div className={`p-2 rounded-xl transition-all ${isOpen ? 'bg-rose-100 text-rose-600 rotate-180' : 'bg-gray-50 text-gray-400'}`}><ChevronDown className="w-4 h-4" /></div></button>{isOpen && <div className="px-6 pb-6 pt-0 text-gray-600 text-sm font-medium leading-relaxed animate-in slide-in-from-top-2 duration-300"><div className="pt-4 border-t border-gray-50">{faq.answer}</div></div>}</div>);})}</div></div>))}</div>
    </div>
  );
};