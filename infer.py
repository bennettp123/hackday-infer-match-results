import boto3
import argparse
import json
import pandas as pd


# only used when --enpoint-name is omitted
DEFAULT_ENDPOINT = \
    'canvas-predict-score-difference-trimmed-full-08-07-2024-5-01-PM'


def get_predictions(matches):
    sagemaker_runtime = boto3.client('runtime.sagemaker')

    # convert to csv
    data = pd.DataFrame.from_records(matches)
    body = data.to_csv(
        columns=['home_team_id', 'away_team_id', 'venue_id'],
        index=False,
        header=False,
    )

    # invoke model to get predictions
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=args.endpoint_name,
        ContentType="text/csv",
        Body=bytes(body, encoding='utf-8'),
        Accept="application/json"
    )

    # parse response
    response_json = json.loads(response['Body'].read().decode('utf-8'))
    predictions = response_json['predictions']

    return predictions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--home-team-id', type=int, required=True)
    parser.add_argument('--away-team-id', type=int, required=True)
    parser.add_argument('--venue-id', type=int, required=True)
    parser.add_argument('--endpoint-name', type=str, default=DEFAULT_ENDPOINT)
    args = parser.parse_args()

    matches = [
        {
            'home_team_id': args.home_team_id,
            'away_team_id': args.away_team_id,
            'venue_id': args.venue_id,
        },
        # ... more records (optional)
    ]

    predictions = get_predictions(matches)

    # print predicted results
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
