// Get chatbot elements
const chatbot = document.getElementById('chatbot');
const conversation = document.getElementById('conversation');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('input-field');

// Add event listener to input form
inputForm.addEventListener('submit', function(event) {
  // Prevent form submission
  event.preventDefault();

  // Get user input
  const input = inputField.value;

  // Clear input field
  inputField.value = '';
  const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

  // Add user input to conversation
  let message = document.createElement('div');
  message.classList.add('chatbot-message', 'user-message');
  message.innerHTML = <p class="chatbot-text" sentTime="${currentTime}">${input}</p>;
  conversation.appendChild(message);

  // Generate chatbot response
  const response = generateResponse(input);

  // Add chatbot response to conversation
  message = document.createElement('div');
  message.classList.add('chatbot-message', 'chatbot');
  message.innerHTML = <p class="chatbot-text" sentTime="${currentTime}">${response}</p>;
  conversation.appendChild(message);
  message.scrollIntoView({ behavior: "smooth" });
});

// Training data with keyword-based matching
const trainingData = [
  { keywords: ["hi", "hello", "hey"], response: "Hello, how can I help you today? 😊" },
  { keywords: ["name", "who are you", "your name"], response: "My name is Waterbot. I'm here to assist you with any questions or problems you may have. How can I help you today? 🚀" },
  { keywords: ["water cycle","explain", "explain the water cycle"], response: "The water cycle describes the continuous movement of water on, above, and below the Earth's surface. It involves processes like evaporation, condensation, precipitation, and runoff." },
  { keywords: ["important","importance", "benefits", "why water"], response: "Water is essential for all known forms of life. It is crucial for drinking, agriculture, sanitation, and various industrial processes. It also helps regulate the Earth's temperature." },
  { keywords: ["conserve water", "water conservation", "save water"], response: "You can conserve water by fixing leaks, using water-efficient appliances, taking shorter showers, turning off the tap while brushing your teeth, and collecting rainwater for gardening." },
  { keywords: ["cause","causes","pollution", "water polution", "water contamination"], response: "Water pollution is caused by contaminants entering water bodies. Common sources include industrial discharge, agricultural runoff, sewage, and plastic waste. It can harm aquatic life and human health." },
  { keywords: ["different states", "states of water", "water states"], response: "Water exists in three states: solid (ice), liquid (water), and gas (water vapor). It can change states through processes like melting, freezing, evaporation, and condensation."},
  { keywords: ["daily water requirements", "water drink per day"], response: "The recommended daily water intake varies, but a common guideline is to drink about 8 glasses (2 liters) of water per day. Individual needs may vary based on activity level, climate, and health conditions."},
  { keywords: ["ph is high", "ph too high", "dealing high water ph", "handle high water ph"], response: "If the water pH is too high, you can add acids like muriatic acid or vinegar to lower it."},
  { keywords: ["correcting low water ph", "fix low water ph", "ph is too low"], response: "If the water pH is too low, you can add alkaline substances like baking soda or soda ash to raise it."},
  { keywords: ["maintaining proper ph level", "maintaining ph"], response: "Maintaining proper pH levels is important because it ensures the safety and effectiveness of the water for its intended use."},
  { keywords: ["ph range for drinking water", "ph for safe drinking water"], response: "The ideal pH range for drinking water is between 6.5 and 8.5."},
  { keywords: ["test ph level", "methods to test ph", "testing ph"], response: "You can test the pH level of water using pH test strips, a pH meter, or a water testing kit."},
  { keywords: ["hard water", "explain hard water"], response: "Hard water is water that contains high levels of dissolved minerals, primarily calcium and magnesium."},
  { keywords: ["causes of water hardness", "maked water hard"], response: "Water hardness is caused by the presence of dissolved minerals, mainly calcium and magnesium, which are picked up as water passes through rocks and soil."},
  { keywords: ["water hardness measured", "assessing hard water", "measuring hard water"], response: "Water hardness is typically measured in milligrams per liter (mg/L) or parts per million (ppm) of calcium carbonate (CaCO3). It can also be expressed in grains per gallon (gpg)."},
  { keywords: ["effects of hard water", "hard water affects on plumbing and appliances", "consequences of hard water"], response: "Hard water can cause scale buildup in pipes and appliances, reduce the efficiency of soaps and detergents, and may leave spots on dishes and clothing."},
  { keywords: ["soften hard water", "reduces hardness"], response: "Hard water can be softened using a water softener, which typically uses ion exchange to replace calcium and magnesium ions with sodium or potassium ions."},
  { keywords: ["hard water safe to drink", "consume hard water", "drink hard water"], response: "Yes, hard water is generally safe to drink. However, it can cause aesthetic issues like taste and scale buildup. In some cases, people with dietary sodium restrictions may need to consider alternative treatments if using a sodium-based water softener."},
  { keywords: ["benefits hard water", "advantages of hard water"], response: "Hard water contains essential minerals like calcium and magnesium, which can contribute to dietary intake. Some studies suggest that hard water may have cardiovascular benefits."},
  { keywords: ["disadvantages of hard water", "demerits of hard water", "drawbacks of hard water"], response: "Disadvantages of hard water include scale buildup in pipes and appliances, reduced efficiency of soaps and detergents, and potential spots on dishes and clothing. It can also shorten the lifespan of water-using appliances."},
  { keywords: ["affects of hard water on skin", "affects of hard water on hair"], response: "Yes, hard water can affect skin and hair. It can leave a residue that may make skin feel dry and hair look dull. Some people may also experience skin irritation."},
  { keywords: ["temporary hardness", "water is temporarily hard"], response: "Temporary hardness is caused by dissolved bicarbonate minerals that can be removed by boiling the water. This process converts bicarbonates into insoluble carbonates, which can then be filtered out."},
  { keywords: ["permanent hardness", "water permanent hard"], response: "Permanent hardness is caused by dissolved sulfate or chloride compounds of calcium and magnesium. This type of hardness cannot be removed by boiling and typically requires a water softener to treat."},
  { keywords: ["water softner works", "softening hard water working"], response: "A water softener works by using ion exchange to replace calcium and magnesium ions in the water with sodium or potassium ions. This process reduces the hardness of the water."},
  { keywords: ["concerns for water softner", "water softner safe for health"], response: "Water softeners that use sodium can increase the sodium content of the water, which may be a concern for people on low-sodium diets. Potassium-based softeners are an alternative."},
  { keywords: ["types of softners", "varities of softner"], response: "The main types of water softeners are salt-based ion exchange softeners, salt-free water conditioners, reverse osmosis systems, and magnetic or electronic descalers."},
  { keywords: ["solid states of water", "different solid states"], response: "The different solid states of water include ice and snow. Ice forms when water freezes, and snow forms when water vapor condenses directly into ice crystals in the atmosphere."},
  { keywords: ["temperature of water to ice", "turning water to ice"], response: "Water turns into ice at 0 degrees Celsius (32 degrees Fahrenheit) under standard atmospheric pressure."},
  { keywords: ["structure of ice", "ice structure"], response: "The structure of ice is a crystalline lattice where water molecules are arranged in a regular pattern. This structure makes ice less dense than liquid water, which is why ice floats."},
  { keywords: ["water freezing pressure", "freezing point of water"], response: "Increasing pressure can lower the freezing point of water. This phenomenon is used in ice skating and in the formation of glaciers, where the pressure of the ice above causes the ice below to melt and refreeze."},
  { keywords: ["ice existence", "different forms of ice"], response: "Yes, ice can exist in different forms called polymorphs or phases, depending on the temperature and pressure conditions. The most common form of ice is Ice Ih, but there are other forms such as Ice II, Ice III, and so on, each with a different crystal structure."},
  { keywords: ["frost", "define frost"], response: "Frost is a thin layer of ice that forms on solid surfaces when water vapor from the air condenses and freezes. It typically forms on cold, clear nights when the temperature of surfaces drops below the freezing point."},
  { keywords: ["icebergs", "icebergs made of"], response: "Icebergs are made of freshwater ice that has broken off from glaciers or ice shelves. They can float in the ocean because the density of ice is lower than that of seawater."},
  { keywords: ["snow form", "snow formation"], response: "Snow forms when water vapor in the atmosphere condenses directly into ice crystals, bypassing the liquid phase. These ice crystals then cluster together to form snowflakes, which fall to the ground when they become heavy enough."},
  { keywords: ["glacier", "define glaciers"], response: "A glacier is a large, slow-moving mass of ice formed from compacted layers of snow. Glaciers form in areas where more snow falls in winter than melts in summer, and they can flow under their own weight due to gravity."},
  { keywords: ["melting of ice", "ice melt", "ice melt causes"], response: "Ice melts when it absorbs enough heat to break the hydrogen bonds between water molecules, causing the solid structure to collapse and turn into liquid water. This typically occurs at temperatures above 0 degrees Celsius (32 degrees Fahrenheit)."},
  { keywords: ["black ice", "define black ice"], response: "Black ice is a thin, transparent layer of ice that forms on roads and sidewalks. It is difficult to see because it blends in with the surface beneath it, making it particularly hazardous for driving and walking."},
  { keywords: ["water freezing temperature"], response: "Under normal atmospheric pressure, water freezes at 0°C. However, under high pressure or in the presence of impurities, water can freeze at temperatures slightly above 0°C."},
  { keywords: ["define chloramines", "chloramines found"], response: "Chloramines are disinfectants used to treat drinking water. They are formed when ammonia is added to chlorine to treat drinking water and are used as an alternative to chlorine."},
  { keywords: ["Chloramines in water treatement", "effective disinfectants"], response: "Chloramines are used in water treatment because they are more stable and longer-lasting than chlorine, providing continued disinfection as water moves through the pipes."},
  { keywords: ["chloramines formation", "ammonia in chloramine formation"], response: "Chloramines are formed when ammonia is added to chlorine in a specific ratio during the water treatment process. This combination creates a disinfectant that is more stable than chlorine alone."},
  { keywords: ["chloramines in drinking water", "effectiveness of chloramines in water"], response: "Yes, chloramines are considered safe for use in drinking water by health authorities such as the EPA. They effectively disinfect water and have been used for many years in water treatment."},
  { keywords: ["cause of chloramines in health", "chloramines safe for health"], response: "At the levels used in drinking water, chloramines are not known to cause health issues. However, some people may experience skin irritation or respiratory issues if they are sensitive to chloramines."},
  { keywords: ["chloramines in swimming pool", "chloramines safe for skin in swimming"], response: "Swimming in water treated with chloramines is generally safe, but some individuals might experience skin or eye irritation. Proper pool maintenance can minimize these effects."},
  { keywords: ["chloramine in plumbing", "causes of chloramines on pipes"], response: "Chloramines can cause leaching of lead and copper in household plumbing, particularly if the pipes are old or corroded. It is important to monitor and manage water chemistry to prevent these issues."},
  { keywords: ["chloramine in water heater","chloramines damage heater"], response: "Chloramines are not known to cause significant damage to water heaters. However, regular maintenance and monitoring can help ensure the longevity of your appliances."},
  { keywords: ["remove chloramines", "eliminating chloramines"], response: "Chloramines can be removed from water using activated carbon filters, which adsorb the chloramines. Additionally, reverse osmosis systems and certain chemical treatments can effectively remove chloramines."},
];

// Generate chatbot response function
function generateResponse(input) {
  // Convert input to lowercase for case insensitivity
  const lowerCaseInput = input.toLowerCase();

  // Check input against training data for keyword matches
  for (const { keywords, response } of trainingData) {
    for (const keyword of keywords) {
      if (lowerCaseInput.includes(keyword)) {
        return response;
      }
    }
  }

  // Return "I'm sorry" if no specific keyword is matched
  return "I'm sorry, I didn't understand your question. Could you please rephrase it? 😕";
}

// Tab switch alert
window.onblur = function() {
  alert('Trying to switch tabs, eh!');
};