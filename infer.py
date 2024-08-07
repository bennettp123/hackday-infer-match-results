import boto3
import argparse
import json


# only used when --enpoint-name is omitted
DEFAULT_ENDPOINT = \
    'canvas-predict-score-difference-trimmed-full-08-07-2024-5-01-PM'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--home-team-id', type=int, required=True)
    parser.add_argument('--away-team-id', type=int, required=True)
    parser.add_argument('--venue-id', type=int, required=True)
    parser.add_argument('--endpoint-name', type=str, default=DEFAULT_ENDPOINT)

    args = parser.parse_args()

    client = boto3.client('runtime.sagemaker')

    body = {
        "features": [
            int(args.home_team_id),
            int(args.away_team_id),
            int(args.venue_id),
        ]
    }

    response = client.invoke_endpoint(
        EndpointName=args.endpoint_name,
        ContentType="application/json",
        Body=bytes(json.dumps(body), encoding='utf-8'),
        Accept="application/json"
    )

    response_json = json.loads(response['Body'].read().decode('utf-8'))
    predictions = response_json['predictions']

    for prediction in predictions:
        score = int(prediction['score'])
        if score == 0:
            print('Prediction: a draw!')
        elif score > 0:
            winner = 'home team'
            margin = f'{score} points'
        else:
            winner = 'away team'
            margin = f'{-score} points'

        print(f'Prediction: {winner} to win by {margin}')
