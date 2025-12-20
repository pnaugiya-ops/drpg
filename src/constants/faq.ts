export interface FAQItem {
  id: string;
  category: string;
  question: string;
  answer: string;
}

export const FAQS: FAQItem[] = [
  {
    id: "f1",
    category: "Pregnancy",
    question: "How many scans are needed?",
    answer: "Usually 3–4 scans during pregnancy."
  },
  {
    id: "f2",
    category: "Infertility",
    question: "When is ovulation period?",
    answer: "Typically day 11–17 of a 28-day cycle."
  }
];
