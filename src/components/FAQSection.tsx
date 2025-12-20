import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import { FAQS } from "../constants";

export const FAQSection: React.FC = () => {
  const [openId, setOpenId] = useState<string | null>(null);

  const categories = Array.from(
    new Set(FAQS.map((faq) => faq.category))
  );

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-center">
        FAQs
      </h2>

      {categories.map((category) => (
        <div key={category}>
          <h3 className="font-semibold text-rose-600">
            {category}
          </h3>

          {FAQS.filter(f => f.category === category).map(faq => (
            <div key={faq.id} className="border rounded-xl my-2">
              <button
                className="w-full flex justify-between p-4"
                onClick={() =>
                  setOpenId(openId === faq.id ? null : faq.id)
                }
              >
                {faq.question}
                <ChevronDown
                  className={openId === faq.id ? "rotate-180" : ""}
                />
              </button>

              {openId === faq.id && (
                <div className="px-4 pb-4 text-gray-600">
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};
