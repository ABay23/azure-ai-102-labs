import os
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
endpoint = os.getenv("ENDPOINT_URL", "https://alejandrobay-699-resource.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
    
# Initialize Azure OpenAI client with Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-01-01-preview",
)


# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a history teacher who can answer questions about past events all around the world."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "what are the key events in the history of Venezuela?"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Venezuela has a rich and complex history shaped by indigenous civilizations, European colonization, independence movements, and modern political developments. Here are some key events in the history of Venezuela:\n\n### **Pre-Columbian Era**\n- **Indigenous Civilizations (Before 1498)**: Venezuela was inhabited by various indigenous groups, including the Caribs, Arawaks, and Timoto-Cuicas. These groups lived off agriculture, fishing, and hunting and had distinct cultures and social structures.\n\n### **Colonial Period**\n- **1498: Arrival of Christopher Columbus**: Columbus arrived on Venezuela's eastern coast during his third voyage. This marked the beginning of European exploration in the region.\n- **1528: Spanish Colonization Begins**: Spain began establishing settlements in Venezuela, including Nueva Toledo (Cumaná) and Caracas. Indigenous resistance, disease, and exploitation marked this period.\n- **1546–1556: Rebellion of the Indigenous Leader Guaicaipuro**: Guaicaipuro led resistance against Spanish colonizers but was ultimately defeated.\n- **16th–18th Centuries**: Venezuela became part of the Spanish colonial system, focusing on agriculture, particularly cacao production. African slaves were brought to work on plantations.\n\n### **Independence Movement**\n- **1810: Venezuelan War of Independence Begins**: Inspired by the American and French Revolutions, Venezuelans sought independence from Spain. The First Republic of Venezuela was established but quickly fell due to internal divisions and Spanish counterattacks.\n- **1811: Declaration of Independence**: Venezuela declared independence, becoming the first South American country to do so. However, independence struggles persisted for years.\n- **1813–1814: Bolívar's \"Admirable Campaign\"**: Simón Bolívar, the key figure in Latin American independence, led a campaign to liberate Venezuela from Spanish rule.\n- **1821: Battle of Carabobo**: Bolívar's forces won a decisive victory against Spain, securing Venezuela's independence. Venezuela became part of Gran Colombia, a union of northern South American countries.\n\n### **Post-Independence Era**\n- **1830: Dissolution of Gran Colombia**: Venezuela separated from Gran Colombia and became an independent republic.\n- **19th Century: Political Turmoil**: Venezuela experienced frequent civil wars, coups, and dictatorships as factions struggled for power.\n- **1870–1888: Guzmán Blanco's Rule**: Antonio Guzmán Blanco modernized Venezuela, building infrastructure and promoting education, though his rule was authoritarian.\n\n### **20th Century**\n- **1908–1935: Dictatorship of Juan Vicente Gómez**: Gómez ruled Venezuela with an iron fist, suppressing dissent but stabilizing the economy. During his rule, Venezuela became one of the world's largest oil exporters.\n- **1920s: Discovery of Oil**: Oil was discovered in Venezuela, transforming its economy and making it a major player in global petroleum markets.\n- **1945: First Democratic Coup**: A civilian-military alliance overthrew the government, leading to the establishment of democracy.\n- **1958: Fall of Marcos Pérez Jiménez**: The dictatorship of Pérez Jiménez ended after widespread protests, and Venezuela transitioned to democracy.\n- **1958–1998: Democratic Era**: Venezuela experienced relative political stability during this period, marked by alternating governments and strong economic growth fueled by oil exports.\n\n### **Modern Era**\n- **1992: Hugo Chávez's Coup Attempt**: Chávez, a military officer, led an unsuccessful coup against the government but gained popularity.\n- **1998: Election of Hugo Chávez**: Chávez was elected president, launching the \"Bolivarian Revolution,\" which implemented socialist policies and nationalized key industries, especially oil.\n- **2002: Failed Coup Against Chávez**: A brief coup removed Chávez from power, but he was reinstated after massive protests.\n- **2013: Death of Hugo Chávez**: Chávez passed away, and Nicolás Maduro became president.\n- **2014–Present: Economic and Political Crisis**: Venezuela faced hyperinflation, shortages of basic goods, political unrest, and mass emigration. Maduro's presidency has been marked by accusations of authoritarianism and international sanctions.\n\n### **Key Cultural and Social Developments**\n- **Oil Boom (20th Century)**: Venezuela became one of the wealthiest nations in Latin America, attracting immigrants from Europe and neighboring countries.\n- **Social Movements**: Indigenous rights, labor unions, and women's movements have played significant roles in shaping modern Venezuelan society.\n\nVenezuela's history is characterized by cycles of prosperity and upheaval, with oil playing a central role in its economy and politics."
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=6553,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.to_json())