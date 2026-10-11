# Pharmacy location mix-up

**Start here: [failed run 1, readable prompt and tool trace](original-listing-ten-native-20261011/FAILED-RUN-01.md).** The agent returned “9:00 PM” using a Mission Street listing for the user’s Castro request.

All three new batches use fresh native background gpt-6.1-sol agents and the same local mock client. The address and weekday closing time remain 2389 Mission Street and 9 PM.

| Question / returned name | Completed replies | Gave a time without a warning | Gave a time but warned it was unconfirmed | Withheld the time or asked for the address |
|---|---:|---:|---:|---:|
| [On Castro Street / explicit Mission Street branch](castro-street-ten-20261011/RESULTS.md) | 10 | 0 | 0 | 10 |
| [On Castro / explicit Mission Street branch](on-castro-ten-20261011/RESULTS.md) | 9 | 0 | 0 | 9 |
| [On castro / Baywell Pharmacy, address only](original-listing-ten-native-20261011/RESULTS.md) | 10 | 5 | 1 | 4 |

The middle batch had ten attempts: one stalled after retrieving the listing and was interrupted without a final reply. Its partial trace is preserved; it is not counted as a supported or unsupported answer.

The original-listing batch reproduces the earlier wrong-location attribution behavior using native agents. Earlier CLI trials are a separate experiment. These are descriptive small batches, not population error rates. No source supplies Castro’s actual closing time; the failure is an unsupported location-specific answer.

Each folder preserves its fixture, pre-dispatch manifest, client, run traces and audit. These traces are included in this repository.
