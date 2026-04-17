# Commit Examples

## Fix auth expiry

Kém:

```text
fix: fix the issue where expired tokens are still being accepted
```

Tốt:

```text
fix(auth): reject expired jwt
```

## Retry on 429

Kém:

```text
feat: add retry logic for the external API when it returns rate limited responses
```

Tốt:

```text
feat(api): retry 429 with backoff
```

## Breaking route rename

```text
feat(api)!: rename checkout endpoint

BREAKING CHANGE: `/v1/orders` is replaced by `/v1/checkout`.
Clients must migrate before the next release.
```

## Migration note

```text
refactor(db): split user profile table

Keep old columns readable for one release to support rollback.
```
