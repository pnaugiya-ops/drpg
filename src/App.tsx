// src/App.tsx
import { ChatInterface } from "./components/ChatInterface";
import { FAQSection } from "./components/FAQSection";

export default function App() {
  return (
    <div className="p-6 space-y-10">
      <ChatInterface onBack={() => {}} />
      <FAQSection />
    </div>
  );
}
