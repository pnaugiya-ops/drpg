import React, { useEffect, useState } from 'react';
import { Calendar, FileText, Activity, MessageCircle, Clock, Stethoscope, Pill, Plus, CheckCircle2, Utensils, Calculator, HeartPulse, RefreshCw, Sparkles, Users, Video, Share2, Baby, Star, Scissors } from 'lucide-react';
import { Appointment, Report, User, SocialPost } from '../types';
import { Button } from './CoreUI';
import { generateDailyTip } from '../services/geminiService.';

export const PatientDashboard: React.FC<{ user: User; reports: Report[]; appointments: Appointment[]; posts: SocialPost[]; onNavigate: (v: any) => void; }> = ({ user, reports, appointments, posts, onNavigate }) => {
  const myAppointments = appointments.filter(a => a.patientId === user.id);
  const nextAppointment = myAppointments.sort((a,b) => new Date(a.date).getTime() - new Date(b.date).getTime())[0];
  const [dailyTip, setDailyTip] = useState<string>('Welcome to your specialist portal.');
  const [loadingTip, setLoadingTip] = useState(false);

  useEffect(() => {
    const fetchTip = async () => {
        setLoadingTip(true);
        try {
          const context = user.isPregnant ? "pregnant" : "managing wellness and fertility";
          const tip = await generateDailyTip(context);
          setDailyTip(tip);
        } catch (e) { setDailyTip("Focus on your health today."); }
        finally { setLoadingTip(false); }
    };
    fetchTip();
  }, [user.isPregnant]);

  return (
    <div className="space-y-8 pb-8 animate-medical-in">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-rose-600 to-purple-600">Welcome, {user.name}</h1>
          <p className="text-gray-500 mt-1 font-medium">{user.isPregnant ? "Monitoring your pregnancy journey" : "Specialist Women's Care Portal"}</p>
        </div>
        <div className="flex flex-wrap gap-3">
             <Button onClick={() => window.open('https://api.whatsapp.com/send?phone=919676712517', '_blank')} className="bg-[#25D366] border-0 shadow-none"><MessageCircle className="w-4 h-4 mr-2" />WhatsApp</Button>
             <Button onClick={() => onNavigate('symptom-checker')} variant="secondary"><Stethoscope className="w-4 h-4 mr-2" />Check Symptoms</Button>
            <Button onClick={() => onNavigate('chat')}><Sparkles className="w-4 h-4 mr-2" />AI Assistant</Button>
        </div>
      </header>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-gradient-to-r from-violet-50 to-purple-50 p-6 rounded-3xl border border-violet-100 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-4">
              <div className="bg-white p-3 rounded-2xl text-violet-600 shadow-sm"><Sparkles className="w-6 h-6" /></div>
              <div>
                <h4 className="text-xs font-bold text-violet-600 uppercase tracking-wider">Daily Wellness Insight</h4>
                <p className="text-base font-semibold text-gray-800">{loadingTip ? "Consulting AI..." : dailyTip}</p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-rose-500 to-pink-600 rounded-[2.5rem] p-8 shadow-xl text-white relative overflow-hidden group">
            <div className="relative z-10 flex flex-col md:flex-row items-start justify-between">
              <div className="space-y-4">
                <div className="inline-flex items-center px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-semibold"><Calendar className="w-3 h-3 mr-2" />Upcoming Visit</div>
                {nextAppointment ? (
                  <div className="space-y-2">
                    <div className="text-4xl font-black">{new Date(nextAppointment.date).toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}</div>
                    <div className="flex items-center text-lg text-rose-100 font-medium"><Clock className="w-5 h-5 mr-2" />{nextAppointment.time} &bull; {nextAppointment.type}</div>
                  </div>
                ) : (
                  <div>
                    <p className="text-xl font-bold mb-4">Ready for your next checkup?</p>
                    <Button onClick={() => onNavigate('booking')} variant="outline" className="bg-white text-rose-600 border-0 shadow-none">Request Appointment</Button>
                  </div>
                )}
              </div>
              {nextAppointment && <div className="mt-6 md:mt-0"><span className="inline-flex items-center px-4 py-1.5 rounded-full bg-white text-rose-600 font-black text-xs shadow-sm uppercase tracking-widest">Confirmed Visit<CheckCircle2 className="w-4 h-4 ml-2" /></span></div>}
            </div>
            <Activity className="absolute -right-8 -bottom-8 w-48 h-48 opacity-10" />
          </div>
        </div>

        <div className="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-black text-gray-900 italic uppercase text-sm tracking-widest">Journey Progress</h3>
              <Star className="text-yellow-400 fill-yellow-400" size={18} />
            </div>
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center text-rose-500"><Baby size={24} /></div>
                <div className="flex-1">
                  <div className="flex justify-between text-xs font-bold mb-1"><span className="text-gray-400 uppercase">Trimester 1</span><span className="text-rose-600">65% Complete</span></div>
                  <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden"><div className="h-full bg-rose-500 rounded-full" style={{ width: '65%' }} /></div>
                </div>
              </div>
              <p className="text-xs text-gray-500 font-medium leading-relaxed">You are doing great! Your next scan is expected between week 11-13.</p>
            </div>
          </div>
          <Button variant="outline" fullWidth size="sm" onClick={() => onNavigate('calculator')} className="mt-6">View Timeline</Button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {[
          { id: 'reports', label: 'History', icon: <FileText className="text-blue-600" />, bg: 'bg-blue-50', border: 'border-blue-100' },
          { id: 'pharmacy', label: 'Pharmacy', icon: <Pill className="text-emerald-600" />, bg: 'bg-emerald-50', border: 'border-emerald-100' },
          { id: user.isPregnant ? 'calculator' : 'cycle-tracker', label: user.isPregnant ? 'Due Date' : 'Fertility Map', icon: <Calculator className="text-pink-600" />, bg: 'bg-pink-50', border: 'border-pink-100' },
          { id: 'diet', label: 'Diet Plan', icon: <Utensils className="text-orange-600" />, bg: 'bg-orange-50', border: 'border-orange-100' },
          { id: 'vitals', label: 'My Vitals', icon: <HeartPulse className="text-cyan-600" />, bg: 'bg-cyan-50', border: 'border-cyan-100' },
          { id: 'surgery-guide', label: 'Surgery', icon: <Activity className="text-teal-600" />, bg: 'bg-teal-50', border: 'border-teal-100' }
        ].map(item => (
          <div key={item.id} onClick={() => onNavigate(item.id)} className={`${item.bg} p-6 rounded-[2.5rem] border ${item.border} cursor-pointer hover:shadow-lg transition-all flex flex-col items-center text-center group`}>
            <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center mb-4 shadow-sm group-hover:scale-110 transition-transform">{item.icon}</div>
            <h3 className="font-black text-gray-900 text-[10px] uppercase tracking-widest">{item.label}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export const DoctorDashboard: React.FC<{ appointments: Appointment[]; onShare: () => void; }> = ({ appointments, onShare }) => {
  const todayStr = new Date().toISOString().split('T')[0];
  const daysAppointments = appointments.filter(a => a.date.startsWith(todayStr)).sort((a,b) => a.time.localeCompare(b.time));

  return (
    <div className="space-y-6 animate-medical-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div><h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-blue-600">Specialist Portal</h1><p className="text-gray-500 font-medium">Dr. Priyanka Gupta | Gynae & Laparoscopy</p></div>
        <div className="flex items-center gap-3">
           <Button onClick={onShare} variant="secondary"><Share2 className="w-4 h-4 mr-2" />Invite Patient</Button>
           <Button onClick={() => {}}><Plus className="w-4 h-4 mr-2" />New Entry</Button>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
             <div className="p-6 border-b border-gray-50 bg-gray-50/30 flex justify-between items-center"><h3 className="font-bold text-gray-900 flex items-center"><Calendar className="w-5 h-5 mr-2 text-rose-500" />Today's Visits</h3></div>
             <div className="divide-y divide-gray-50 min-h-[400px]">
                {daysAppointments.length > 0 ? daysAppointments.map((apt) => (
                    <div key={apt.id} className="p-6 flex items-center justify-between group hover:bg-slate-50 transition-colors">
                        <div className="flex items-start gap-4">
                            <div className="flex-shrink-0 w-20 text-center py-3 bg-blue-50 rounded-2xl border border-blue-100"><span className="block text-xl font-black text-blue-700">{apt.time.split(' ')[0]}</span><span className="block text-[10px] font-bold text-blue-400 uppercase">{apt.time.split(' ')[1]}</span></div>
                            <div><h3 className="font-black text-gray-900 text-lg">{apt.patientName}</h3><p className="text-sm text-gray-500"><span className="bg-white px-2 py-0.5 rounded-lg text-xs border border-gray-200">{apt.type}</span></p></div>
                        </div>
                        <Button variant="outline" size="sm">Manage</Button>
                    </div>
                )) : <div className="p-12 text-center text-gray-400 font-medium">No appointments scheduled for today.</div>}
             </div>
        </div>
        <div className="space-y-6">
            <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-[2.5rem] p-8 border border-indigo-100">
                <h3 className="font-bold text-indigo-900 mb-6 flex items-center uppercase text-xs tracking-widest"><Users className="w-5 h-5 mr-2" />Clinic Metrics</h3>
                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white p-5 rounded-[1.5rem] border shadow-sm text-center"><span className="block text-3xl font-black text-indigo-600">{daysAppointments.length}</span><span className="text-[10px] text-gray-400 uppercase font-black">Patients</span></div>
                    <div className="bg-white p-5 rounded-[1.5rem] border shadow-sm text-center"><span className="block text-3xl font-black text-rose-600">3</span><span className="text-[10px] text-gray-400 uppercase font-black">Surgery</span></div>
                    <div className="bg-white p-5 rounded-[1.5rem] border shadow-sm text-center col-span-2"><span className="block text-3xl font-black text-teal-600">12</span><span className="text-[10px] text-gray-400 uppercase font-black">Infertility Mapping Cases</span></div>
                </div>
            </div>
            <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
              <h3 className="font-black text-gray-900 mb-4 flex items-center uppercase text-xs tracking-widest"><Video className="w-5 h-5 mr-2 text-rose-500" />Education Feed</h3>
              <p className="text-sm text-gray-500 font-medium mb-6">Upload surgery demos or health tips for your patients to view.</p>
              <Button size="sm" fullWidth>Create New Post</Button>
            </div>
        </div>
      </div>
    </div>
  );
};