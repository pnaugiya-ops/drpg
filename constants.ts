
import { Appointment, Report, User, VitalStat, FAQItem, SocialPost, Service, Prescription, DietPlan, ExercisePlan, CycleData } from './types';

export const MOCK_PATIENT: User = {
  id: 'p1',
  name: 'Sarah Johnson',
  role: 'patient',
  avatarUrl: 'https://picsum.photos/id/64/200/200',
  age: '29',
  dob: '1995-05-20',
  address: 'B-14, Green Park Extension, New Delhi',
  phoneNumber: '+91 98765 43210',
  aadhaarUrl: '', // Empty by default
  isPregnant: true // Default setting for demonstration
};

export const MOCK_DOCTOR: User = {
  id: 'd1',
  name: 'Dr. Priyanka Gupta',
  role: 'doctor',
  avatarUrl: 'https://picsum.photos/id/65/200/200',
};

export const CLINIC_SERVICES: Service[] = [
  { id: 's1', title: 'Consultation', description: 'Expert Gynae & Obstetrics advice' },
  { id: 's2', title: 'Ultrasound', description: 'High-res imaging diagnostics' },
  { id: 's3', title: 'Transvaginal Scanning', description: 'Detailed pelvic examination' },
  { id: 's4', title: 'Obstetrics Growth Scan', description: 'Fetal development tracking' },
  { id: 's5', title: 'Bhavya Labs', description: 'Comprehensive blood tests' },
  { id: 's6', title: 'Pharmacy', description: 'All Gynae & Obs medicines available' },
  { id: 's7', title: 'Infertility Care', description: 'IVF & IUI Treatment' },
  { id: 's8', title: 'Laparoscopy', description: 'Minimally Invasive Surgery' },
];

export const DEFAULT_CYCLE_DATA: CycleData = {
    lastPeriodDate: new Date().toISOString().split('T')[0], // Default to today if not set
    cycleLength: 28,
    periodDuration: 5
};

export const MOCK_PRESCRIPTIONS: Prescription[] = [
  { 
    id: 'rx_avinate', 
    medication: 'Avinate', 
    dosage: '1 Tablet', 
    instruction: 'Daily at night after food', 
    date: new Date().toISOString().split('T')[0], 
    active: true,
    description: 'Combination of Folic Acid and vomiting medication. Specifically for first trimester.'
  },
  { 
    id: 'rx_dronyx', 
    medication: 'Dronyx', 
    dosage: '10mg', 
    instruction: 'Twice a day after food', 
    date: new Date().toISOString().split('T')[0], 
    active: true,
    description: 'Prescribed for high-risk pregnancies.'
  },
  { 
    id: 'rx_proliks', 
    medication: 'Proliks Mom Protein Powder', 
    dosage: '2 Scoops', 
    instruction: 'Morning and evening in one glass of milk', 
    date: new Date().toISOString().split('T')[0], 
    active: true,
    description: 'Protein supplement specifically for pregnant patients.'
  },
  { 
    id: 'rx_fero', 
    medication: 'Fero Pink', 
    dosage: '1 Tablet', 
    instruction: 'Daily once before lunch (Course: 1 Month)', 
    date: new Date().toISOString().split('T')[0], 
    active: true,
    description: 'Iron supplement.'
  },
  { 
    id: 'rx_calci', 
    medication: 'Calci K27', 
    dosage: '1 Tablet', 
    instruction: 'One hour after breakfast', 
    date: new Date().toISOString().split('T')[0], 
    active: true,
    description: 'Calcium supplement.'
  },
  { id: 'rx_history_1', medication: 'Progesterone', dosage: '200mg', instruction: 'Before bed', date: '2023-09-01', active: false },
];

export const UPCOMING_APPOINTMENTS: Appointment[] = [
  {
    id: 'a1',
    patientId: 'p1',
    patientName: 'Sarah Johnson',
    date: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
    time: '10:00 AM',
    type: 'Ultrasound',
    status: 'upcoming',
    notes: '20-week anomaly scan',
  },
  {
    id: 'a2',
    patientId: 'p2',
    patientName: 'Rebecca Smith',
    date: new Date(Date.now() + 172800000).toISOString(), // Day after tomorrow
    time: '02:30 PM',
    type: 'Consultation',
    status: 'upcoming',
    notes: 'Infertility treatment follow-up',
  },
  {
    id: 'a3',
    patientId: 'p3',
    patientName: 'Monica Geller',
    date: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
    time: '11:15 AM',
    type: 'Checkup',
    status: 'upcoming',
    notes: 'Routine trimester check',
  },
];

export const PATIENT_REPORTS: Report[] = [
  {
    id: 'r1',
    patientId: 'p1',
    title: 'Complete Blood Count (CBC)',
    date: '2023-10-15',
    type: 'Blood',
    summary: 'Hemoglobin levels normal (12.5 g/dL).',
  },
  {
    id: 'r2',
    patientId: 'p1',
    title: 'Trimester 1 Ultrasound',
    date: '2023-09-01',
    type: 'Ultrasound',
    imageUrl: 'https://picsum.photos/id/200/400/300',
    summary: 'Fetal heartbeat detected. Crown-rump length normal.',
  },
  {
    id: 'r3',
    patientId: 'p1',
    title: 'Thyroid Profile',
    date: '2023-08-15',
    type: 'Blood',
    summary: 'TSH within normal range.',
  },
];

export const VITAL_TRENDS: VitalStat[] = [
  { date: 'Aug', value: 11.2, unit: 'g/dL', label: 'Hemoglobin' },
  { date: 'Sep', value: 11.8, unit: 'g/dL', label: 'Hemoglobin' },
  { date: 'Oct', value: 12.5, unit: 'g/dL', label: 'Hemoglobin' },
  { date: 'Nov', value: 12.1, unit: 'g/dL', label: 'Hemoglobin' },
];

export const DOCTOR_SPECIALTIES = [
  "Gynecologist",
  "Obstetrician",
  "Infertility Specialist",
  "Laparoscopic Surgeon"
];

export const FAQS: FAQItem[] = [
  {
    id: 'f1',
    category: 'Pregnancy',
    question: 'When should I schedule my first prenatal visit?',
    answer: 'It is recommended to schedule your first prenatal appointment as soon as you think you might be pregnant, ideally around 8 weeks from your last menstrual period.',
  },
  {
    id: 'f2',
    category: 'Pregnancy',
    question: 'Is it safe to exercise during pregnancy?',
    answer: 'Generally, yes. Moderate exercise like walking or swimming is beneficial. However, always consult with Dr. Gupta before starting any new exercise routine.',
  },
  {
    id: 'f3',
    category: 'Infertility',
    question: 'When should we seek help for infertility?',
    answer: 'If you are under 35 and have been trying to conceive for a year, or over 35 and trying for 6 months, we recommend scheduling a consultation.',
  },
  {
    id: 'f4',
    category: 'General Health',
    question: 'How often should I get a Pap smear?',
    answer: 'Women ages 21 to 65 should generally get a Pap smear every 3 years. If combined with HPV testing, it can be every 5 years for those over 30.',
  }
];

export const SOCIAL_POSTS: SocialPost[] = [
  {
    id: 's1',
    type: 'youtube',
    url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', // Placeholder
    caption: 'Understanding Laparoscopic Surgery: Benefits & Recovery',
  },
  {
    id: 's2',
    type: 'youtube',
    url: 'https://www.youtube.com/embed/36YnV9STBqc', // Placeholder
    caption: 'Tips for a Healthy Pregnancy Trimester by Trimester',
  },
  {
    id: 's3',
    type: 'instagram',
    url: 'https://picsum.photos/id/1025/300/300', 
    thumbnail: 'https://picsum.photos/id/1025/300/300',
    caption: 'Welcoming another beautiful baby girl to the world today! 🎀 #ObGynLife #Newborn',
  },
  {
    id: 's4',
    type: 'instagram',
    url: 'https://picsum.photos/id/1062/300/300', 
    thumbnail: 'https://picsum.photos/id/1062/300/300',
    caption: 'Discussing fertility options at the annual medical conference. 🏥',
  },
];

export const PREGNANCY_DIET_PLANS: DietPlan[] = [
  {
    trimester: 1,
    title: "Trimester 1 (Weeks 1-12)",
    description: "Focus on Folic Acid, Vitamin B6 for nausea, and hydration. Small frequent meals are key.",
    vegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Soaked Almonds (5-6)', 'Walnuts (2)', 'Dry Toast or Biscuit (if nauseous)'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Vegetable Poha/Upma with lots of veggies', '1 Cup Milk', 'Fresh Fruit (Apple/Banana)'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Coconut Water', 'Roasted Makhana (Fox nuts)'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['2 Multigrain Roti', '1 Bowl Dal/Lentils', '1 Bowl Green Vegetable', 'Salad', 'Curd'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Vegetable Soup', 'Cheese Slice or Roasted Chana'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Khichdi with Ghee', 'Or 1-2 Roti with Lauki/Torai Sabzi', 'Cucumber Salad'], icon: 'moon' },
    ],
    nonVegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Soaked Almonds (5-6)', 'Walnuts (2)', 'Dry Toast'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['2 Boiled Eggs or Omelette', 'Whole Wheat Toast', '1 Cup Milk'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Coconut Water', 'Fruit Chat'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['2 Roti', 'Chicken Curry (Mild Spices)', 'Vegetable Salad', 'Curd'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Clear Chicken Soup', 'Boiled Egg (if not had in breakfast)'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Steamed Fish', 'Sautéed Vegetables', '1 Small Bowl Rice'], icon: 'moon' },
    ]
  },
  {
    trimester: 2,
    title: "Trimester 2 (Weeks 13-26)",
    description: "Crucial for Calcium, Iron, and Vitamin D. Baby's bone development accelerates.",
    vegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Glass of Warm Milk', 'Soaked Almonds & Figs'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Paneer Paratha (Less Oil)', 'Curd', 'Fruit Juice'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Sprout Salad', 'Buttermilk (Chaas)'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['2 Roti', 'Palak Paneer', 'Rajma/Chole', 'Beetroot Salad'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Mixed Fruit Bowl with Seeds', 'Smoothie'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Mixed Vegetable Curry', '2 Roti', 'Dal'], icon: 'moon' },
    ],
    nonVegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Glass of Warm Milk', 'Soaked Almonds & Figs'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Scrambled Eggs with Spinach', 'Toast', 'Orange Juice'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Chicken Salad', 'Yogurt'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['2 Roti', 'Mutton Curry (Occasional) or Fish Curry', 'Dal', 'Rice'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Grilled Chicken Sandwich', 'Fruit'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Grilled Fish', 'Mashed Potato', 'Green Beans'], icon: 'moon' },
    ]
  },
  {
    trimester: 3,
    title: "Trimester 3 (Weeks 27-40)",
    description: "High energy requirements. Focus on Vitamin K and Omega-3. Eat lighter dinners to avoid heartburn.",
    vegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Dates (2)', 'Walnuts', 'Milk'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Oats Porridge with Fruits', 'Or Idli Sambar'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Carrot/Beetroot Juice', 'Roasted Pumpkin Seeds'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['Rice/Roti', 'Soya Chunk Curry', 'Leafy Greens', 'Curd'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Corn/Sweet Potato Chaat'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Vegetable Dalia', 'Tomato Soup', 'Light Salad'], icon: 'moon' },
    ],
    nonVegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Dates (2)', 'Walnuts', 'Milk'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Egg White Omelette', 'Whole Wheat Bread', 'Apple'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Bone Broth or Chicken Soup'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['Rice/Roti', 'Lean Meat Curry', 'Vegetables', 'Raita'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Boiled Egg Salad'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Grilled Chicken Breast', 'Quinoa/Rice', 'Steamed Veggies'], icon: 'moon' },
    ]
  }
];

export const PCOS_DIET_PLANS: DietPlan[] = [
  {
    title: "PCOS Management (General)",
    description: "Focus on Low Glycemic Index (GI) foods to improve insulin sensitivity. High fiber, anti-inflammatory foods, and avoiding processed sugars.",
    vegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Warm Water with Lemon & Honey', 'Soaked Methi (Fenugreek) Seeds'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['Moong Dal Chilla with Mint Chutney', 'Or Oats Upma with Veggies'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Green Tea', 'Small bowl of Papaya or Apple'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['1 Multigrain Roti (Jowar/Bajra)', 'Bowl of Dal', 'Green Leafy Vegetable', 'Salad (Cucumber/Tomato)'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Roasted Makhana or Chana', 'Handful of Pumpkin Seeds'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Grilled Paneer Salad', 'Or Quinoa Khichdi with Veggies', 'Buttermilk'], icon: 'moon' },
    ],
    nonVegetarian: [
      { time: '07:00 AM', label: 'Early Morning', items: ['Warm Water with Lemon', 'Soaked Walnuts (2)'], icon: 'sunrise' },
      { time: '09:00 AM', label: 'Breakfast', items: ['2 Egg Whites Omelette with Spinach', 'Whole Grain Toast'], icon: 'coffee' },
      { time: '11:00 AM', label: 'Mid-Morning', items: ['Green Tea', 'Pear or Berries'], icon: 'sun' },
      { time: '01:30 PM', label: 'Lunch', items: ['1 Multigrain Roti', 'Chicken Curry (Less Oil)', 'Salad', 'Curd'], icon: 'sun' },
      { time: '05:00 PM', label: 'Evening Snack', items: ['Boiled Egg', 'Green Tea'], icon: 'sunset' },
      { time: '08:00 PM', label: 'Dinner', items: ['Grilled Fish', 'Sautéed Broccoli & Beans', 'Clear Soup'], icon: 'moon' },
    ]
  }
];

export const PREGNANCY_EXERCISE_PLANS: ExercisePlan[] = [
  {
    trimester: 1,
    title: "Trimester 1 (Weeks 1-12)",
    focus: "Gentle Mobility & Stability",
    description: "Focus on maintaining activity levels while respecting your body's new changes. Listen to your body and avoid overheating.",
    exercises: [
      {
        id: 'e1_1',
        name: 'Walking',
        description: 'Brisk walking on a flat surface. Keep your shoulders back and head up.',
        duration: '20-30 mins daily',
        benefits: 'Improves cardiovascular health without joint stress.',
        intensity: 'Low',
        safetyNote: 'Wear comfortable shoes and stay hydrated.'
      },
      {
        id: 'e1_2',
        name: 'Pelvic Floor (Kegels)',
        description: 'Tighten pelvic muscles as if stopping urine flow. Hold for 5s, release.',
        duration: '10 reps, 3 times a day',
        benefits: 'Strengthens pelvic floor to support uterus and bladder.',
        intensity: 'Low'
      },
      {
        id: 'e1_3',
        name: 'Butterfly Stretch',
        description: 'Sit with feet together, knees out. Gently press knees down.',
        duration: 'Hold for 30 seconds',
        benefits: 'Opens up the hips and improves flexibility.',
        intensity: 'Low'
      }
    ]
  },
  {
    trimester: 2,
    title: "Trimester 2 (Weeks 13-26)",
    focus: "Strength & Posture",
    description: "Energy levels usually return. Good time for moderate strength training and yoga. Avoid lying flat on your back.",
    exercises: [
      {
        id: 'e2_1',
        name: 'Prenatal Yoga',
        description: 'Cat-Cow pose, Warrior II, and Modified Triangle pose.',
        duration: '30 mins session',
        benefits: 'Improves balance, flexibility, and mental calm.',
        intensity: 'Medium',
        safetyNote: 'Avoid deep twists and lying on your back.'
      },
      {
        id: 'e2_2',
        name: 'Squats (Supported)',
        description: 'Stand with feet shoulder-width apart. Lower down as if sitting in a chair, holding a support.',
        duration: '2 sets of 10 reps',
        benefits: 'Strengthens legs and opens the pelvis for labor.',
        intensity: 'Medium',
        safetyNote: 'Keep your back straight and heels on the floor.'
      },
      {
        id: 'e2_3',
        name: 'Swimming',
        description: 'Gentle laps or water aerobics.',
        duration: '20 mins',
        benefits: 'Relieves weight from joints and reduces swelling.',
        intensity: 'Medium'
      }
    ]
  },
  {
    trimester: 3,
    title: "Trimester 3 (Weeks 27-40)",
    focus: "Preparation for Labor",
    description: "Slow down as the baby grows. Focus on opening the hips and breathing techniques.",
    exercises: [
      {
        id: 'e3_1',
        name: 'Pelvic Tilts',
        description: 'On hands and knees, gently arch your back up and then flatten it to neutral.',
        duration: '10-15 reps',
        benefits: 'Relieves back pain and helps position the baby.',
        intensity: 'Low'
      },
      {
        id: 'e3_2',
        name: 'Wall Push-ups',
        description: 'Stand facing a wall, place hands on it, and gently push body towards and away.',
        duration: '10 reps',
        benefits: 'Upper body strength for holding the baby.',
        intensity: 'Low'
      },
      {
        id: 'e3_3',
        name: 'Deep Breathing',
        description: 'Diaphragmatic breathing. Inhale deeply through nose, exhale slowly through mouth.',
        duration: '5 mins daily',
        benefits: 'Reduces stress and prepares for labor breathing.',
        intensity: 'Low'
      }
    ]
  }
];

export const PCOS_EXERCISE_PLANS: ExercisePlan[] = [
  {
    title: "PCOS Fitness Routine",
    focus: "Metabolism & Hormone Balance",
    description: "A combination of cardio and strength training is best for managing insulin resistance and aiding weight loss.",
    exercises: [
      {
        id: 'pcos_1',
        name: 'HIIT (High Intensity Interval Training)',
        description: 'Alternating short bursts of intense activity with rest periods (e.g., Jumping Jacks, Burpees).',
        duration: '20 mins (3 times a week)',
        benefits: 'Boosts insulin sensitivity and burns calories effectively.',
        intensity: 'High',
        safetyNote: 'Start slow if you are a beginner.'
      },
      {
        id: 'pcos_2',
        name: 'Strength Training',
        description: 'Using weights or resistance bands. Focus on compound movements like squats and lunges.',
        duration: '30 mins (2 times a week)',
        benefits: 'Builds muscle mass which helps burn glucose.',
        intensity: 'Medium'
      },
      {
        id: 'pcos_3',
        name: 'Yoga (Supta Baddha Konasana)',
        description: 'Reclining Bound Angle Pose. Lie on back, feet together, knees open.',
        duration: 'Hold for 2-5 mins',
        benefits: 'Reduces stress (cortisol) and stimulates abdominal organs.',
        intensity: 'Low'
      }
    ]
  }
];