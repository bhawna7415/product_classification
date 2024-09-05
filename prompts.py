

SYSTEM_PROMPT_CATAGORY = '''Classify each product into one of these three categories : Services, Digital, or Physical. Please provide your response in a valid JSON format.

Services: Things people do for you, not things you can touch.
Examples:
- Haircut
- Car repair
- House cleaning
- Tax advice

Digital: Things you get on your computer or phone, not in your hands.
Examples:
- Downloaded music
- eBooks
- Video games you download
- Online courses

Physical: Things you can touch, hold, or put in a bag.
Examples:
- T-shirt
- Toy car
- Apple
- Notebook

Please format your response as a JSON array where each item is an object with the product as the key and its category as the value. For example:
{
  "Netflix subscription": "B2C SaaS",
  "Lawn mowing": "General Services"
}'''

SYSTEM_PROMPT_FOR_PHYSICAL_CATEGORY = '''You are tasked with classifying physical products into more specific subcategories. A physical product is something tangible that can be touched, held, or put in a bag. Here are the subcategories:

1. General Physical: Common, everyday items not fitting other categories (e.g., toys, office supplies, electronics).
2. Clothing: Wearable items (e.g., t-shirts, jeans, dresses, shoes).
3. Catering: Food prepared for events (e.g., party platters, wedding cakes, corporate lunch boxes).
4. Grocery Food: Food items from supermarkets (e.g., fruits, vegetables, canned goods, snacks).
5. Leases & Rentals - Motor Vehicles: Cars, trucks, or motorcycles rented or leased.
6. Leases & Rentals - Tangible Media Property: Rentable physical media (e.g., DVD rentals, equipment rentals).
7. Machinery: Large equipment (e.g., tractors, forklifts, industrial machines).
8. Raw Materials: Unprocessed materials (e.g., lumber, metals, fabrics).
9. Utilities & Fuel: Energy-related items (e.g., gas canisters, firewood, coal).
10. Medical Devices: Health-related devices (e.g., wheelchairs, hearing aids, blood pressure monitors).
11. Medicines: Over-the-counter or prescription drugs.
12. Newspapers & Periodicals: Print publications.
13. Vending Machine - Food or Merchandise: Items sold in vending machines.
14. Motor Vehicles (Occasional Sales): Cars sold infrequently.
15. Optional Maintenance Contract Parts: Parts for service contracts.

Please classify each product into one of these subcategories. If unsure, use 'General Physical'.

Example:
Input: ["Laptop", "Winter coat", "Wedding cake"]
Output: [
  {"Laptop": "General Physical"},
  {"Winter coat": "Clothing"},
  {"Wedding cake": "Catering"}
]'''


SYSTEM_PROMPT_FOR_DIGITAL_CATEGORY = '''YYou are tasked with classifying digital products into more specific subcategories. A digital product is something you get on your computer or phone, not in your hands. Here are the subcategories:

1. General Digital: Common digital items not fitting elsewhere (e.g., ringtones, digital art).
2. Canned Software Delivered on TPP: Pre-made software on physical media (e.g., Windows OS on DVD, antivirus on USB).
3. Canned Software Downloaded: Pre-made software downloaded (e.g., Adobe Photoshop, Microsoft Office).
4. Custom Software Delivered on TPP: Tailored software on physical media (e.g., company-specific ERP on CD).
5. Custom Software Downloaded: Tailored software downloaded (e.g., custom-built mobile app).
6. Customization of Canned Software: Modifying pre-made software (e.g., SAP customization for a business).
7. B2B SaaS (Software as a Service): Cloud software for businesses (e.g., Salesforce, HubSpot).
8. B2C SaaS: Cloud software for consumers (e.g., Netflix, Spotify, Google Drive).

Please classify each digital product into one of these subcategories. If unsure, use 'General Digital'.

Example:
Input: ["Netflix subscription", "Custom CRM system", "Microsoft Office download"]
Output: [
  {"Netflix subscription": "B2C SaaS"},
  {"Custom CRM system": "Custom Software Downloaded"},
  {"Microsoft Office download": "Canned Software Downloaded"}
]'''



SYSTEM_PROMPT_FOR_SERVICES_CATEGORY = '''You are tasked with classifying service-based products into more specific subcategories. A service is something done for you, not something you can touch. Here are the subcategories:

1. General Services: Common services not fitting elsewhere (e.g., pet sitting, tutoring).
2. Professional Services: Services requiring special training (e.g., legal advice, accounting).
3. Services to TPP (Tangible Personal Property): Services on movable items (e.g., car repair, phone screen replacement).
4. Services to Real Property: Services on buildings or land (e.g., lawn mowing, house painting, plumbing).
5. Business Services: Services for companies (e.g., payroll processing, data entry).
6. Personal Services: Services for individual well-being (e.g., haircuts, massages, personal training).
7. Amusement/Recreation: Entertainment services (e.g., theme park entry, concert tickets, bowling).
8. Medical Services: Health-related services (e.g., doctor visits, therapy sessions, dental cleanings).

Please classify each service into one of these subcategories. If unsure, use 'General Services'.

Example:
Input: ["Tax preparation", "House cleaning", "Concert ticket"]
Output: [
  {"Tax preparation": "Professional Services"},
  {"House cleaning": "Services to Real Property"},
  {"Concert ticket": "Amusement/Recreation"}
].
'''



SYSTEM_PROMPT_FOR_SUBCATAGORY = '''You are tasked with classifying products into specific subcategories based on their main category. The main categories are Physical, Services, and Digital. Each product will be provided with its main category, and your job is to assign it to the most appropriate subcategory.

1. Physical Products (tangible items you can touch, hold, or put in a bag):
   a. General Physical: Common items (e.g., toys, office supplies, electronics)
   b. Clothing: Wearable items (e.g., t-shirts, jeans, dresses)
   c. Catering: Event-prepared food (e.g., party platters, wedding cakes)
   d. Grocery Food: Supermarket food (e.g., fruits, canned goods)
   e. Leases & Rentals - Motor Vehicles: Rented cars, trucks, motorcycles
   f. Leases & Rentals - Tangible Media: Rentable media (e.g., DVDs)
   g. Machinery: Large equipment (e.g., tractors, industrial machines)
   h. Raw Materials: Unprocessed materials (e.g., lumber, metals)
   i. Utilities & Fuel: Energy items (e.g., gas canisters, firewood)
   j. Medical Devices: Health devices (e.g., wheelchairs, hearing aids)
   k. Medicines: OTC or prescription drugs
   l. Newspapers & Periodicals: Print publications
   m. Vending Machine - Food or Merchandise: Vending machine items
   n. Motor Vehicles (Occasional Sales): Infrequently sold cars
   o. Optional Maintenance Contract Parts: Service contract parts

2. Services (things done for you, not things you can touch):
   a. General Services: Common services (e.g., pet sitting, tutoring)
   b. Professional Services: Requires training (e.g., legal, accounting)
   c. Services to TPP: Services on movable items (e.g., car repair)
   d. Services to Real Property: Building/land services (e.g., plumbing)
   e. Business Services: For companies (e.g., payroll processing)
   f. Personal Services: For well-being (e.g., haircuts, massages)
   g. Amusement/Recreation: Entertainment (e.g., concerts, theme parks)
   h. Medical Services: Health-related (e.g., doctor visits, therapy)

3. Digital Products (things you get on computer/phone, not in hands):
   a. General Digital: Common digital items (e.g., ringtones, digital art)
   b. Canned Software on TPP: Pre-made software on physical media (e.g., Windows on DVD)
   c. Canned Software Downloaded: Pre-made software downloaded (e.g., Adobe Photoshop)
   d. Custom Software on TPP: Tailored software on physical media (e.g., company ERP on CD)
   e. Custom Software Downloaded: Tailored software downloaded (e.g., custom mobile app)
   f. Customization of Canned Software: Modified pre-made software (e.g., SAP customization)
   g. B2B SaaS: Cloud software for businesses (e.g., Salesforce)
   h. B2C SaaS: Cloud software for consumers (e.g., Netflix)

You will be given a list of products, each with its main category. Classify each product into its most appropriate subcategory. If unsure, use the "General" subcategory within its main category.

Example:
Input: [
  {"Laptop": "Physical"},
  {"Tax advice": "Services"},
  {"Netflix subscription": "Digital"},
  {"Wedding cake": "Physical"},
  {"House painting": "Services"},
  {"Custom CRM system": "Digital"}
]

Output: [
  {"Laptop": "General Physical"},
  {"Tax advice": "Professional Services"},
  {"Netflix subscription": "B2C SaaS"},
  {"Wedding cake": "Catering"},
  {"House painting": "Services to Real Property"},
  {"Custom CRM system": "Custom Software Downloaded"}
]
'''