# usage

Not for production use.

```bash
# build the image
docker build -t infer-results .

# run the image
docker run --rm -it \
  -v ~/.aws:/root/.aws:ro -e AWS_PROFILE=devdigital \
  infer-results --home-team-id <int> --away-team-id <int> --venue-id <int>
```

Alternatively, you can specify AWS creds using `-e AWS_ACCESS_KEY_ID="..." -e AWS_SECRET_ACCESS_KEY="..."`

If the result is positive, then the home team is predicted to be victorious. If negative, the away team is expected to win.

