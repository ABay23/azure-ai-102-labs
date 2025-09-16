import os
from dotenv import load_dotenv; load_dotenv()
from azure.ai.textanalytics import TextAnalyticsClient
from ai102_labs.common.auth import token_credential, key_credential


endpoint = os.environ["LANGUAGE_ENDPOINT"]
cred = key_credential("LANGUAGE_KEY") if os.getenv("LANGUAGE_KEY") else token_credential()

client = TextAnalyticsClient(endpoint=endpoint, credential=cred)
doc = "The API works great, but latency was high."
res = client.analyze_sentiment([doc])[0]
print(res.sentiment, dict(pos=res.confidence_scores.positive,
                        neu=res.confidence_scores.neutral,
                        neg=res.confidence_scores.negative))
