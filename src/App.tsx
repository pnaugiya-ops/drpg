import { ChatInterface } from "./components/ChatInterface";

export function App() {
  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4">
      <ChatInterface onBack={() => {}} />
    </div>
  );
}
