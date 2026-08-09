# South-to-North production transfer study

Two production halls record an intake reading (`feedstock`) and a final
quality score (`outcome`) for every unit. Higher outcome is better; a unit
below 28 is at risk of rejection. Every research table also carries the
routine logistics label `batch_class` (`A` or `B`). Both halls expose the same
operational controls, but the plant does not assume that a model learned at
one site will transfer unchanged to the other.

Your investigation starts in **South**. You can inspect its production archive
and run fresh South trials. Later, the research coordinator will announce the
transfer to **North**. From that point onward you can run North trials. Treat
this as one continuous investigation: keep an executable working model as your
view develops, and use the remaining budget where it is most informative.

In a trial you may set the supplier's `feedstock_grade`, the hall's `humidity`,
both, or neither. A setting left unspecified follows ordinary conditions. The
site is agent-facing context: use `context={"site": "south"}` or
`context={"site": "north"}` as appropriate. Trials ordinarily contain both
routine batch classes. If a class-specific check is needed, add
`"batch_class": "A"` or `"B"` to the context.

Your final submission must define:

```python
def model(regime, n, seed):
    ...
```

It must return exactly a pandas DataFrame with columns `feedstock` and
`outcome`, with `n` simulated rows. Evaluation covers **both South and North**,
may provide `regime.context["batch_class"]`, and may use ordinary conditions
or set either advertised control through `regime.config`; the site is in
`regime.context["site"]`. Model the full distribution, including process
variation, rather than only a mean.
