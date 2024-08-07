import boto3
import pandas as pd

client = boto3.client(
    'runtime.sagemaker',
    region_name='ap-southeast-2',
)

#body = pd.DataFrame([
#    ['home_team_id', 'away_team_id', 'venue_id'],
#    [10, 100, 40],
#]).to_csv(header=True, index=False).encode("utf-8")

body = bytes(
    '{ "features": [ 10, 100, 40 ] }',
    encoding='utf-8',
)

endpoint_name = 'canvas-predict-score-difference-trimmed-full-08-07-2024-5-01-PM'

response = client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=body,
    Accept="application/json"
)

print(response['Body'].read().decode('utf-8'))
