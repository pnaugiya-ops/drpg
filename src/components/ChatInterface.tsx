import React, { useState } from "react";
import { Send, Bot } from "lucide-react";

export const ChatInterface: React.FC<{ onBack: () => void }> = () => {
  const [messages, setMessages] = useState([
    { role: "model", text: "Hello! I'm Dr. Gupta's AI assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-xl bg-white rounded-3xl shadow-2xl border">
      <div className="p-4 border-b flex items-center gap-2">
        <Bot className="text-rose-600" />
        <h2 className="font-bold">AI Concierge</h2>
      </div>

      <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-slate-50">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span
              className={`inline-block px-4 py-2 rounded-2xl ${
                m.role === "user"
                  ? "bg-rose-600 text-white"
                  : "bg-white border"
              }`}
            >
              {m.text}
            </span>
          </div>
        ))}
      </div>

      <div className="p-4 border-t flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 px-4 py-3 bg-gray-100 rounded-xl outline-none"
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          className="bg-rose-600 text-white p-3 rounded-xl"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};
