import { PrismaClient, MapNodeType, EdgeType } from "@prisma/client";

const prisma = new PrismaClient();

// Career families with nodes
const careerData: Array<{
  family: string;
  careers: Array<{
    label: string;
    description: string;
    metadata: Record<string, unknown>;
  }>;
}> = [
  {
    family: "Technology",
    careers: [
      {
        label: "Software Engineer",
        description:
          "Design and build software systems, applications, and platforms.",
        metadata: {
          medianSalary: "$130,000",
          growthRate: "25%",
          educationRequired: "BS Computer Science or related",
          skills: [
            "Programming",
            "Algorithms",
            "System Design",
            "Problem Solving",
          ],
          entryPaths: [
            "CS degree",
            "Bootcamp",
            "Self-taught + portfolio",
            "Internship",
          ],
          dayInTheLife:
            "Writing code, reviewing PRs, debugging, team standups, designing features",
        },
      },
      {
        label: "Product Manager",
        description:
          "Own the vision, strategy, and roadmap of a product from conception to launch.",
        metadata: {
          medianSalary: "$140,000",
          growthRate: "19%",
          educationRequired: "Any bachelor's degree",
          skills: [
            "Strategy",
            "Communication",
            "Data Analysis",
            "Empathy",
            "Prioritization",
          ],
          entryPaths: ["APM programs", "MBA", "Internal transfer", "Startup"],
          dayInTheLife:
            "User interviews, writing specs, coordinating with engineering, reviewing metrics",
        },
      },
      {
        label: "UX/UI Designer",
        description:
          "Create user experiences and interfaces that are intuitive, accessible, and beautiful.",
        metadata: {
          medianSalary: "$105,000",
          growthRate: "23%",
          educationRequired: "BS Design/HCI or portfolio equivalent",
          skills: [
            "Visual Design",
            "Prototyping",
            "User Research",
            "Figma",
            "Empathy",
          ],
          entryPaths: [
            "Design degree",
            "Bootcamp",
            "Self-taught",
            "Art + CS combo",
          ],
          dayInTheLife:
            "Wireframing, user testing, collaborating with PM and engineers, iterating designs",
        },
      },
      {
        label: "Data Scientist",
        description:
          "Extract insights from large datasets to inform decisions and build predictive models.",
        metadata: {
          medianSalary: "$126,000",
          growthRate: "35%",
          educationRequired: "BS/MS Statistics, Math, CS, or related",
          skills: [
            "Python",
            "Statistics",
            "Machine Learning",
            "SQL",
            "Communication",
          ],
          entryPaths: ["STEM degree", "Kaggle competitions", "Research", "MS"],
          dayInTheLife:
            "Data wrangling, model building, presenting findings, A/B testing",
        },
      },
      {
        label: "AI/ML Engineer",
        description:
          "Build and deploy machine learning systems and AI applications at scale.",
        metadata: {
          medianSalary: "$155,000",
          growthRate: "40%",
          educationRequired: "BS/MS Computer Science or Statistics",
          skills: [
            "Deep Learning",
            "PyTorch/TensorFlow",
            "MLOps",
            "Math",
            "Python",
          ],
          entryPaths: ["CS/Math degree", "Research lab", "Online courses", "MS/PhD"],
          dayInTheLife:
            "Training models, infrastructure optimization, reading papers, deployment",
        },
      },
    ],
  },
  {
    family: "Finance",
    careers: [
      {
        label: "Investment Banking Analyst",
        description:
          "Advise companies on mergers, acquisitions, and capital raising transactions.",
        metadata: {
          medianSalary: "$120,000",
          growthRate: "10%",
          educationRequired: "BS Finance, Economics, Math",
          skills: [
            "Financial Modeling",
            "Excel",
            "Valuation",
            "Presentations",
            "Stamina",
          ],
          entryPaths: ["Target school recruiting", "Summer analyst programs", "Networking"],
          dayInTheLife: "Building models, creating pitch decks, client calls, due diligence",
        },
      },
      {
        label: "Venture Capitalist",
        description:
          "Identify and invest in promising early-stage startups, guiding them to success.",
        metadata: {
          medianSalary: "$200,000+",
          growthRate: "15%",
          educationRequired: "BS + operational experience or MBA",
          skills: [
            "Pattern Recognition",
            "Founder Empathy",
            "Network Building",
            "Market Analysis",
          ],
          entryPaths: [
            "Operator → VC",
            "Banking → VC",
            "MBA",
            "Scout program",
          ],
          dayInTheLife: "Sourcing deals, founder meetings, board prep, portfolio support",
        },
      },
      {
        label: "Quantitative Analyst",
        description:
          "Apply mathematics and statistical models to financial markets and risk management.",
        metadata: {
          medianSalary: "$175,000",
          growthRate: "18%",
          educationRequired: "MS/PhD Math, Physics, CS, or Statistics",
          skills: ["Mathematics", "Programming", "Statistics", "Finance", "C++/Python"],
          entryPaths: ["PhD program", "MS Quant Finance", "Math Olympiad background"],
          dayInTheLife: "Building pricing models, risk analysis, backtesting, research",
        },
      },
    ],
  },
  {
    family: "Healthcare",
    careers: [
      {
        label: "Physician",
        description: "Diagnose and treat patients across a wide range of medical conditions.",
        metadata: {
          medianSalary: "$208,000",
          growthRate: "13%",
          educationRequired: "MD (4 years med school + residency)",
          skills: ["Clinical Knowledge", "Empathy", "Decision Making", "Communication"],
          entryPaths: ["Premed → MCAT → MD → Residency"],
          dayInTheLife: "Patient rounds, diagnoses, procedures, charting, teaching",
        },
      },
      {
        label: "Biomedical Engineer",
        description:
          "Design medical devices, equipment, and systems that improve human health.",
        metadata: {
          medianSalary: "$98,000",
          growthRate: "11%",
          educationRequired: "BS Biomedical Engineering",
          skills: ["Engineering", "Biology", "CAD", "FDA Regulations", "Materials Science"],
          entryPaths: ["BME degree", "ME + biology coursework", "Med device internship"],
          dayInTheLife: "Device design, testing, regulatory prep, cross-functional teams",
        },
      },
      {
        label: "Healthcare Policy Analyst",
        description:
          "Research and develop policies to improve healthcare systems and access.",
        metadata: {
          medianSalary: "$78,000",
          growthRate: "14%",
          educationRequired: "BS Public Health + MPH or MPP",
          skills: ["Research", "Policy Writing", "Data Analysis", "Stakeholder Communication"],
          entryPaths: ["Public health degree", "Government internship", "Think tank"],
          dayInTheLife: "Policy research, report writing, stakeholder meetings, advocacy",
        },
      },
    ],
  },
  {
    family: "Engineering",
    careers: [
      {
        label: "Civil Engineer",
        description:
          "Design and oversee construction of infrastructure like roads, bridges, and buildings.",
        metadata: {
          medianSalary: "$88,000",
          growthRate: "7%",
          educationRequired: "BS Civil Engineering + PE license",
          skills: ["Structural Analysis", "CAD", "Project Management", "Math", "Physics"],
          entryPaths: ["CE degree", "Internship", "PE exam", "Construction experience"],
          dayInTheLife: "Site visits, design reviews, client meetings, compliance checks",
        },
      },
      {
        label: "Aerospace Engineer",
        description:
          "Design aircraft, spacecraft, satellites, and related systems.",
        metadata: {
          medianSalary: "$126,000",
          growthRate: "6%",
          educationRequired: "BS/MS Aerospace Engineering",
          skills: ["Aerodynamics", "Propulsion", "Materials", "Math", "Systems Thinking"],
          entryPaths: ["AE degree", "NASA internship", "Defense contractor", "SpaceX/Blue Origin"],
          dayInTheLife: "CFD simulation, design iteration, testing, cross-team collaboration",
        },
      },
    ],
  },
  {
    family: "Law",
    careers: [
      {
        label: "Corporate Attorney",
        description:
          "Advise businesses on legal matters, contracts, mergers, and compliance.",
        metadata: {
          medianSalary: "$185,000",
          growthRate: "10%",
          educationRequired: "JD (3 years law school after undergrad)",
          skills: ["Legal Research", "Writing", "Negotiation", "Analysis", "Attention to Detail"],
          entryPaths: ["Any UG degree → LSAT → JD → BigLaw"],
          dayInTheLife: "Contract drafting, client counseling, due diligence, court prep",
        },
      },
      {
        label: "Public Defender",
        description:
          "Represent clients who cannot afford legal counsel in criminal proceedings.",
        metadata: {
          medianSalary: "$65,000",
          growthRate: "10%",
          educationRequired: "JD",
          skills: ["Advocacy", "Empathy", "Research", "Oral Arguments", "Case Management"],
          entryPaths: ["JD → Public Defender Office → Caseload"],
          dayInTheLife: "Client meetings, court appearances, case prep, community work",
        },
      },
    ],
  },
  {
    family: "Education",
    careers: [
      {
        label: "Teacher",
        description:
          "Educate and inspire students at K-12 or postsecondary level.",
        metadata: {
          medianSalary: "$62,000",
          growthRate: "5%",
          educationRequired: "BS Education or subject + teaching certification",
          skills: ["Communication", "Patience", "Curriculum Design", "Empathy", "Classroom Management"],
          entryPaths: ["Education degree", "Alt certification", "TFA", "Subject expertise + cert"],
          dayInTheLife: "Lesson planning, teaching, grading, parent communication, professional development",
        },
      },
      {
        label: "Educational Researcher",
        description:
          "Study how people learn to improve educational outcomes and systems.",
        metadata: {
          medianSalary: "$76,000",
          growthRate: "8%",
          educationRequired: "PhD Education or Cognitive Science",
          skills: ["Research Methods", "Statistics", "Writing", "Policy Knowledge", "Data Analysis"],
          entryPaths: ["Education PhD", "Policy fellowship", "Think tank research"],
          dayInTheLife: "Designing studies, analyzing data, writing papers, presenting findings",
        },
      },
    ],
  },
  {
    family: "Media & Communications",
    careers: [
      {
        label: "Journalist",
        description:
          "Investigate, report, and communicate stories of public importance.",
        metadata: {
          medianSalary: "$55,000",
          growthRate: "3%",
          educationRequired: "BS Journalism or related field",
          skills: ["Writing", "Storytelling", "Research", "Source Building", "Multimedia"],
          entryPaths: ["Journalism degree", "Campus newspaper", "Digital first", "Freelance"],
          dayInTheLife: "Reporting, interviewing, writing, fact-checking, pitching stories",
        },
      },
      {
        label: "Documentary Filmmaker",
        description:
          "Create long-form visual storytelling on real-world subjects and issues.",
        metadata: {
          medianSalary: "$70,000",
          growthRate: "12%",
          educationRequired: "BFA Film or self-taught portfolio",
          skills: ["Cinematography", "Storytelling", "Editing", "Research", "Persistence"],
          entryPaths: ["Film school", "Short films", "Festival circuit", "Journalism background"],
          dayInTheLife: "Pre-production research, shooting, editing, festival submissions, pitching",
        },
      },
    ],
  },
  {
    family: "Government & Policy",
    careers: [
      {
        label: "Policy Analyst",
        description:
          "Research and evaluate policies to advise governments and advocacy organizations.",
        metadata: {
          medianSalary: "$75,000",
          growthRate: "9%",
          educationRequired: "BS Political Science/Economics + MPP preferred",
          skills: ["Research", "Writing", "Quantitative Analysis", "Communication", "Systems Thinking"],
          entryPaths: ["Congressional internship", "Think tank", "Graduate school", "Advocacy org"],
          dayInTheLife: "Policy memos, stakeholder briefings, research reports, coalition meetings",
        },
      },
      {
        label: "Foreign Service Officer",
        description:
          "Represent US interests abroad through diplomacy, consular services, and development.",
        metadata: {
          medianSalary: "$85,000",
          growthRate: "5%",
          educationRequired: "Any bachelor's degree + FSOT exam",
          skills: ["Languages", "Cultural Intelligence", "Negotiation", "Writing", "Adaptability"],
          entryPaths: ["Any degree → FSOT → Oral Assessment → Clearance"],
          dayInTheLife: "Meetings with foreign officials, visa adjudication, reporting cables, events",
        },
      },
    ],
  },
  {
    family: "Science & Research",
    careers: [
      {
        label: "Research Scientist",
        description:
          "Conduct original research to expand knowledge in a scientific field.",
        metadata: {
          medianSalary: "$100,000",
          growthRate: "17%",
          educationRequired: "PhD in relevant field",
          skills: ["Research Design", "Statistical Analysis", "Writing", "Grant Writing", "Domain Expertise"],
          entryPaths: ["PhD program", "Postdoc", "Industry R&D", "National lab"],
          dayInTheLife: "Lab work, data analysis, writing papers, grant applications, conferences",
        },
      },
      {
        label: "Environmental Scientist",
        description:
          "Study and protect the natural environment through field work and policy solutions.",
        metadata: {
          medianSalary: "$76,000",
          growthRate: "8%",
          educationRequired: "BS Environmental Science or related",
          skills: ["Field Research", "Data Analysis", "GIS", "Policy Knowledge", "Communication"],
          entryPaths: ["Env. science degree", "Government agency", "Conservation org", "Consulting"],
          dayInTheLife: "Field sampling, data analysis, report writing, regulatory compliance",
        },
      },
    ],
  },
  {
    family: "Arts & Design",
    careers: [
      {
        label: "Architect",
        description: "Design buildings and spaces that are functional, safe, and aesthetically meaningful.",
        metadata: {
          medianSalary: "$93,000",
          growthRate: "5%",
          educationRequired: "BArch or MArch + licensure",
          skills: ["Spatial Design", "CAD/BIM", "Structural Knowledge", "Client Communication", "Drawing"],
          entryPaths: ["Architecture school", "Internship", "ARE exams", "Licensure"],
          dayInTheLife: "Design development, client presentations, site visits, construction docs",
        },
      },
      {
        label: "Graphic Designer",
        description: "Create visual communications for brands, publications, and digital media.",
        metadata: {
          medianSalary: "$58,000",
          growthRate: "3%",
          educationRequired: "BFA Graphic Design or portfolio equivalent",
          skills: ["Typography", "Color Theory", "Adobe Suite", "Branding", "Client Relations"],
          entryPaths: ["Design school", "Freelance portfolio", "In-house designer", "Agency"],
          dayInTheLife: "Client briefs, concept development, design execution, revisions",
        },
      },
    ],
  },
  {
    family: "Entrepreneurship",
    careers: [
      {
        label: "Startup Founder",
        description: "Start and scale a company from an initial idea to a sustainable business.",
        metadata: {
          medianSalary: "Variable ($0 to unlimited)",
          growthRate: "Always growing",
          educationRequired: "Any background — ideas and execution matter most",
          skills: ["Vision", "Resilience", "Fundraising", "Team Building", "Customer Development"],
          entryPaths: ["YC", "Bootstrapping", "Side project → full-time", "University startup"],
          dayInTheLife: "Customer calls, product decisions, recruiting, investor meetings, firefighting",
        },
      },
      {
        label: "Social Entrepreneur",
        description: "Build mission-driven ventures that address social, environmental, or community problems.",
        metadata: {
          medianSalary: "$85,000",
          growthRate: "20%",
          educationRequired: "Any degree + passion for impact",
          skills: ["Impact Measurement", "Storytelling", "Community Building", "Business Fundamentals"],
          entryPaths: ["Nonprofit experience", "Fellowship", "B-Corp", "Hybrid model startup"],
          dayInTheLife: "Community meetings, grant writing, partner development, program design",
        },
      },
    ],
  },
  {
    family: "Nonprofit & Social Impact",
    careers: [
      {
        label: "Program Director",
        description: "Design, run, and evaluate programs that deliver impact for a nonprofit's mission.",
        metadata: {
          medianSalary: "$72,000",
          growthRate: "11%",
          educationRequired: "BS any field + relevant experience",
          skills: ["Program Design", "Evaluation", "Team Leadership", "Grant Management", "Community Engagement"],
          entryPaths: ["AmeriCorps", "Fellowship", "Direct service → management", "Grad school"],
          dayInTheLife: "Team supervision, program delivery, stakeholder reporting, community events",
        },
      },
    ],
  },
  {
    family: "Consulting",
    careers: [
      {
        label: "Management Consultant",
        description: "Help organizations solve complex business problems and improve performance.",
        metadata: {
          medianSalary: "$145,000",
          growthRate: "14%",
          educationRequired: "BS top school or MBA",
          skills: ["Problem Structuring", "Data Analysis", "Communication", "Project Management", "Adaptability"],
          entryPaths: ["Target school recruiting", "Case interview prep", "MBA → MBB"],
          dayInTheLife: "Case work, client presentations, travel, team collaboration, data analysis",
        },
      },
    ],
  },
];

// Major nodes
const majorData: Array<{
  label: string;
  description: string;
  metadata: Record<string, unknown>;
}> = [
  {
    label: "Computer Science",
    description: "Study of computation, algorithms, data structures, and software systems.",
    metadata: {
      relatedCareers: ["Software Engineer", "AI/ML Engineer", "Data Scientist", "Product Manager"],
      topPrograms: ["MIT", "Stanford", "Carnegie Mellon", "UC Berkeley", "University of Waterloo"],
      coreSubjects: ["Algorithms", "Operating Systems", "Machine Learning", "Databases", "Networking"],
    },
  },
  {
    label: "Economics",
    description: "Study of how individuals, firms, and societies allocate scarce resources.",
    metadata: {
      relatedCareers: ["Policy Analyst", "Investment Banking Analyst", "Quantitative Analyst"],
      topPrograms: ["Harvard", "MIT", "Princeton", "University of Chicago", "Northwestern"],
      coreSubjects: ["Micro/Macroeconomics", "Econometrics", "Game Theory", "Behavioral Economics"],
    },
  },
  {
    label: "Psychology",
    description: "Scientific study of mind, behavior, and human development.",
    metadata: {
      relatedCareers: ["Researcher", "UX Designer", "Counselor", "Policy Analyst"],
      topPrograms: ["Stanford", "Harvard", "Michigan", "UCLA", "Duke"],
      coreSubjects: ["Cognitive Psych", "Developmental Psych", "Social Psych", "Neuroscience"],
    },
  },
  {
    label: "Biology",
    description: "Study of living organisms, from molecular processes to ecosystems.",
    metadata: {
      relatedCareers: ["Physician", "Research Scientist", "Biomedical Engineer", "Environmental Scientist"],
      topPrograms: ["MIT", "Johns Hopkins", "Stanford", "Harvard", "Caltech"],
      coreSubjects: ["Genetics", "Cell Biology", "Ecology", "Biochemistry", "Evolution"],
    },
  },
  {
    label: "Political Science",
    description: "Study of political systems, institutions, behavior, and policy.",
    metadata: {
      relatedCareers: ["Policy Analyst", "Foreign Service Officer", "Journalist", "Lawyer"],
      topPrograms: ["Georgetown", "Harvard", "Princeton", "Yale", "UC Berkeley"],
      coreSubjects: ["Comparative Politics", "International Relations", "Political Theory", "American Politics"],
    },
  },
  {
    label: "Symbolic Systems (Stanford)",
    description: "Interdisciplinary major combining CS, philosophy, psychology, and linguistics to study minds and machines.",
    metadata: {
      university: "Stanford University",
      uniqueFeature: "Explores cognition at the intersection of human and artificial intelligence",
      relatedCareers: ["AI/ML Engineer", "UX Designer", "Researcher", "Product Manager"],
      notableAlumni: ["Reid Hoffman", "Peter Thiel"],
    },
  },
  {
    label: "Systems Engineering (UVA)",
    description: "Interdisciplinary approach to designing complex systems across engineering and policy domains.",
    metadata: {
      university: "University of Virginia",
      uniqueFeature: "Combines technical rigor with human factors and organizational design",
      relatedCareers: ["Management Consultant", "Policy Analyst", "Aerospace Engineer", "Product Manager"],
    },
  },
  {
    label: "Applied Mathematics",
    description: "Mathematical methods and models applied to real-world problems in science, engineering, and finance.",
    metadata: {
      relatedCareers: ["Quantitative Analyst", "Data Scientist", "AI/ML Engineer", "Research Scientist"],
      topPrograms: ["MIT", "Princeton", "Harvard", "Caltech", "UCLA"],
      coreSubjects: ["Linear Algebra", "Differential Equations", "Optimization", "Probability", "Numerical Methods"],
    },
  },
];

// Opportunity / program nodes
const programData: Array<{
  label: string;
  description: string;
  metadata: Record<string, unknown>;
}> = [
  {
    label: "Research Science Institute (RSI)",
    description: "Elite 6-week summer research program at MIT for high school students.",
    metadata: {
      type: "Summer Program",
      location: "MIT, Cambridge MA",
      deadline: "January annually",
      eligibility: "High school juniors",
      focus: "STEM research",
    },
  },
  {
    label: "Congressional App Challenge",
    description: "National competition for US high schoolers to design and code apps.",
    metadata: {
      type: "Competition",
      deadline: "November annually",
      eligibility: "US high school students",
      focus: "Software development",
    },
  },
  {
    label: "National Merit Scholarship",
    description: "Academic scholarship competition based on PSAT/NMSQT scores.",
    metadata: {
      type: "Scholarship",
      deadline: "Junior year PSAT",
      eligibility: "US high school students",
      focus: "Academic achievement",
    },
  },
  {
    label: "Harvard Summer School",
    description: "Academic summer programs for pre-college students at Harvard University.",
    metadata: {
      type: "Summer Program",
      location: "Cambridge, MA",
      deadline: "April annually",
      eligibility: "Rising 10th-12th graders",
      focus: "Various disciplines",
    },
  },
  {
    label: "Regeneron Science Talent Search",
    description: "Prestigious science and math competition for high school seniors.",
    metadata: {
      type: "Competition",
      deadline: "November annually",
      eligibility: "High school seniors",
      focus: "Scientific research",
    },
  },
  {
    label: "DECA International Career Development Conference",
    description: "Business and entrepreneurship competition for high school students worldwide.",
    metadata: {
      type: "Competition",
      deadline: "State competition qualifiers",
      eligibility: "DECA members",
      focus: "Business, marketing, finance",
    },
  },
  {
    label: "Model UN",
    description: "Simulation of United Nations for students to develop diplomacy and public speaking skills.",
    metadata: {
      type: "Program",
      eligibility: "High school students",
      focus: "Diplomacy, public speaking, international relations",
    },
  },
  {
    label: "Coursera — Machine Learning Specialization (Stanford)",
    description: "Online specialization covering machine learning fundamentals taught by Andrew Ng.",
    metadata: {
      type: "Online Course",
      platform: "Coursera",
      duration: "3 months",
      focus: "Machine Learning",
      free: "Audit available",
    },
  },
];

async function main() {
  console.log("🌱 Starting seed...");

  // Create a default school
  const school = await prisma.school.upsert({
    where: { id: "default-school" },
    update: {},
    create: {
      id: "default-school",
      name: "COMPASS Demo School",
      district: "Demo District",
      state: "CA",
      tier: "licensed",
    },
  });

  console.log(`✅ Created school: ${school.name}`);

  // Create industry nodes for each career family
  const industryNodes: Record<string, string> = {};

  for (const family of careerData) {
    const industryNode = await prisma.mapNode.upsert({
      where: { id: `industry-${family.family.toLowerCase().replace(/[^a-z]/g, "-")}` },
      update: {},
      create: {
        id: `industry-${family.family.toLowerCase().replace(/[^a-z]/g, "-")}`,
        type: MapNodeType.INDUSTRY,
        label: family.family,
        description: `Career opportunities in the ${family.family} sector`,
        metadata: {},
      },
    });

    industryNodes[family.family] = industryNode.id;
    console.log(`  ✅ Industry: ${family.family}`);

    // Create career nodes
    for (const career of family.careers) {
      await prisma.mapNode.upsert({
        where: {
          id: `career-${career.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
        },
        update: {},
        create: {
          id: `career-${career.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
          type: MapNodeType.CAREER,
          label: career.label,
          description: career.description,
          metadata: career.metadata,
          parentId: industryNode.id,
        },
      });

      // Edge: industry LEADS_TO career
      await prisma.mapEdge.upsert({
        where: {
          sourceId_targetId: {
            sourceId: industryNode.id,
            targetId: `career-${career.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
          },
        },
        update: {},
        create: {
          sourceId: industryNode.id,
          targetId: `career-${career.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
          edgeType: EdgeType.LEADS_TO,
          weight: 0.9,
        },
      });
    }
  }

  // Create major nodes
  for (const major of majorData) {
    await prisma.mapNode.upsert({
      where: {
        id: `major-${major.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
      },
      update: {},
      create: {
        id: `major-${major.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
        type: MapNodeType.MAJOR,
        label: major.label,
        description: major.description,
        metadata: major.metadata,
      },
    });

    console.log(`  ✅ Major: ${major.label}`);
  }

  // Create program/opportunity nodes
  for (const program of programData) {
    await prisma.mapNode.upsert({
      where: {
        id: `program-${program.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
      },
      update: {},
      create: {
        id: `program-${program.label.toLowerCase().replace(/[^a-z]/g, "-")}`,
        type: MapNodeType.PROGRAM,
        label: program.label,
        description: program.description,
        metadata: program.metadata,
      },
    });

    console.log(`  ✅ Program: ${program.label}`);
  }

  // Add some cross-edges between majors and careers
  const crossEdges: Array<{ from: string; to: string; weight: number; type: EdgeType }> = [
    { from: "major-computer-science", to: "career-software-engineer", weight: 0.95, type: EdgeType.LEADS_TO },
    { from: "major-computer-science", to: "career-ai-ml-engineer", weight: 0.9, type: EdgeType.LEADS_TO },
    { from: "major-computer-science", to: "career-data-scientist", weight: 0.85, type: EdgeType.LEADS_TO },
    { from: "major-computer-science", to: "career-product-manager", weight: 0.6, type: EdgeType.LEADS_TO },
    { from: "major-economics", to: "career-investment-banking-analyst", weight: 0.85, type: EdgeType.LEADS_TO },
    { from: "major-economics", to: "career-policy-analyst", weight: 0.7, type: EdgeType.LEADS_TO },
    { from: "major-economics", to: "career-quantitative-analyst", weight: 0.75, type: EdgeType.LEADS_TO },
    { from: "major-biology", to: "career-physician", weight: 0.8, type: EdgeType.LEADS_TO },
    { from: "major-biology", to: "career-research-scientist", weight: 0.85, type: EdgeType.LEADS_TO },
    { from: "major-biology", to: "career-biomedical-engineer", weight: 0.7, type: EdgeType.LEADS_TO },
    { from: "major-political-science", to: "career-policy-analyst", weight: 0.9, type: EdgeType.LEADS_TO },
    { from: "major-political-science", to: "career-foreign-service-officer", weight: 0.85, type: EdgeType.LEADS_TO },
    { from: "major-applied-mathematics", to: "career-quantitative-analyst", weight: 0.95, type: EdgeType.LEADS_TO },
    { from: "major-applied-mathematics", to: "career-data-scientist", weight: 0.85, type: EdgeType.LEADS_TO },
    { from: "major-symbolic-systems--stanford-", to: "career-ai-ml-engineer", weight: 0.8, type: EdgeType.LEADS_TO },
    { from: "major-symbolic-systems--stanford-", to: "career-ux-ui-designer", weight: 0.7, type: EdgeType.LEADS_TO },
  ];

  for (const edge of crossEdges) {
    try {
      await prisma.mapEdge.upsert({
        where: {
          sourceId_targetId: {
            sourceId: edge.from,
            targetId: edge.to,
          },
        },
        update: {},
        create: {
          sourceId: edge.from,
          targetId: edge.to,
          edgeType: edge.type,
          weight: edge.weight,
        },
      });
    } catch {
      // Node might not exist, skip
    }
  }

  console.log("✅ Cross-edges created");
  console.log("🎉 Seed complete!");
}

main()
  .catch(console.error)
  .finally(async () => {
    await prisma.$disconnect();
  });
