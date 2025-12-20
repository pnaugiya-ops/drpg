import React from "react";

type ChatInterfaceProps = {
  onBack?: () => void;
};

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onBack }) => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AI Concierge</h1>

      <div className="border rounded-lg p-4 mb-4">
        <p className="text-gray-600">Chat interface loaded successfully ✅</p>
      </div>

      {onBack && (
        <button
          onClick={onBack}
          className="px-4 py-2 bg-rose-500 text-white rounded"
        >
          Back
        </button>
      )}
    </div>
  );
};
