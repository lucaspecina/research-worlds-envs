# North Hall production study

North Hall records an intake reading (`feedstock`) and a final quality score
(`outcome`) for every unit. Higher outcome is better; a unit below 28 is at
risk of rejection.

You can inspect the historical production archive and run fresh trials. In a
trial you may set the supplier's `feedstock_grade`, the hall's `humidity`,
both, or neither. A setting left unspecified follows ordinary plant
conditions. Use the evidence you collect to build the best predictive model
of the process under the choices the plant can actually make.

Your final submission must define:

```python
def model(regime, n, seed):
    ...
```

It must return exactly a pandas DataFrame with columns `feedstock` and
`outcome`, with `n` simulated rows. Evaluation may use ordinary conditions or
set either advertised control through `regime.config`. Model the full
distribution, including process variation, rather than only a mean.
