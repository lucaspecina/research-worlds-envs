# North Hall production study

The North Hall line records an intake reading (`feedstock`) and a final quality
score (`outcome`) for every unit. Higher outcome is better; a unit finishing
below the acceptance floor of 25 is rejected at the line's cost.

You may inspect the production history and run fresh trials. A trial may set
any subset of `feedstock_grade`, `humidity`, `temp`, and `line_speed`; settings
left unspecified follow ordinary plant conditions. Use the available evidence
to build the best predictive model of the process.

Your final submission must define:

```python
def model(regime, n, seed):
    ...
```

It must return exactly a pandas DataFrame with columns `feedstock` and
`outcome`, with `n` simulated rows. Evaluation may use ordinary conditions or
set any advertised trial controls through `regime.config`. Model the full
distribution, including process variation, rather than only a mean.
