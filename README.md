# pairs-trading-regime-stability
This project investigates whether a classic pairs trading relationship between two sector peers actually holds consistently over time, using a rolling walk-forward regression to identify when the relationship breaks down.

We use Coca-Cola (KO) and Pepsi (PEP) as a case study for this, first testing for full-history cointegration, then using the aforementioned rolling walk-forward methodology to identify shorter regimes where cointegration is present, and how long they last.

## Motivation

This project was built as a self-directed way to develop practical skills in time-series econometrics, applied to a concrete, well-known trading strategy. 

The project is intentionally scoped (a single pair, a defined set of statistical checks) rather than an attempt at a novel/comprehensive trading strategy. The value here is in the rigour applied to a focused question, not the breadth of ground covered.

## Repo Structure and How to Run

If users wish to clone this repository either to customise it or simply run through it, then they should be aware that it uses Poetry to manage packages. Upon cloning of the repository, the user should run `poetry install` to initiate the environment and install the repository's dependencies. 

This project consists of three numbered notebooks in the `notebooks/` folder. [Notebook 1](notebooks/01_data_pull.ipynb) should be run first as this is where the data used for the rest of the project is downloaded (via the `yfinance` package), processed and saved into the `data/` folder. Beyond this, there is no strict requirement to run [notebook 2](notebooks/02_baseline_cointegration.ipynb) before [notebook 3](notebooks/03_rolling_walkforward.ipynb), however it is strongly recommended that they are read in the correct order to preserve the logical line of thought. 

There is one file in the `helpers/` folder which contains a chunky plotting function that would have been out of place if written directly inside the notebook. Other than this, all custom functions used in the notebooks are written within them.


## Methodology


### 1. Data
- In [notebook 1](notebooks/01_data_pull.ipynb), we obtain data for PEP and KO via the `yfinance` package that pulls data from [Yahoo Finance](https://finance.yahoo.com). We pull this data from 1972-06-01 onwards (Earliest available data for PEP) and ensure to use the auto adjust setting to ensure prices are scaled correctly.

### 2. Baseline Cointegration (full history)
- We begin by modelling the raw prices of both stocks but pivot to log-prices due to the multiplicative nature of stock returns over time. See [notebook 2](notebooks/02_baseline_cointegration.ipynb) for the full justification.
- In order for our cointegration tests to make sense, we first need to ensure that the (log) prices themselves are I(0) or I(1). We do this via an Augmented Dickey-Fuller (ADF) test on the (log) prices and their difference series. Ultimately, both the raw prices and log prices were shown to be I(1) but not I(0).
- To test for cointegration, we must use the Engle-Granger (EG) test which has stricter critical values than ADF that is needed due to the fact that the OLS process is designed to make the residuals look as stationary as possible. The EG test is known to be asymmetric so we ensure that both directions are used in all circumstances. 
- No cointegration was found on the full-history checks.

### 3. Rolling Walk-Forward Search
- It was decided that the rolling walk-forward approach was needed due to the absence of full-history cointegration as it was deemed that regimes may be unstable and short-lived.
- We treat the search as two hypotheses: firstly that there exist periods of cointegration and secondly that these periods can persist for some small period of time after identification. Both of these hypotheses are tested twice with different window parameters in [notebook 3](notebooks/03_rolling_walkforward.ipynb) at a significance level of 10% each.
- We may use ADF on the second test, since the bias issue does not apply as we are testing on data different to what the OLS model is fitted on.
- Each hypothesis contains many comparisons and it is important that we make the necessary corrections to our comparison-wise significance rate to avoid blowing up our family wise error rate (FWER). As such, we pre-determine the number of tests that are ran in each hypothesis and apply Bonferroni corrections to the significance levels.
- As mentioned above, we require that each test pass in both directions, but a finding by Berger in his [1982 paper](https://doi.org/10.1080/00401706.1982.10487774) says that no corrections must be applied here.
- Six total periods of cointegration were found over the two window lengths of 100 and 25, however none of these relationships showed evidence of persisting out of sample.

### 4. Limitations / Known Caveats
- Since our rolling windows overlap heavily, testing for cointegration on overlapping windows is heavily dependent. This means that the bonferroni corrections we are applying are conservative.
- The window length parameters are arbitrary choices. There are separate experiments that we could run to find the optimal parameters here. See [future work](#next-steps-and-future-work) below.
- The cointegration search is likely affected by the winner's curse. Any tests that do pass are likely explained in part by test statistics overperforming their expected values by chance. This means that out of sample weakening is expected to a degree.


## Findings

We found PEP and KO not to be cointegrated in log price over their full history. However, using the rolling search, two periods of 100 days each were tested as cointegrated in 1978 and 1987. We also found a further four periods of 25 days each in 1991, 1992, 2005, and 2020. Despite this, we found no evidence, using the walk-forward analysis, that these regimes held beyond these original test periods.


## Next Steps and Future Work

Such is the nature of this short project, there are many potential avenues for future work here: 
- Expanding the analysis to a broader set of "sector peer" pairs - It is important to remember that this project was conducted on one pair amongst an astronomically large pool of potential pairs. We may even look to conduct a similar cointegration analysis on sets of three or more stocks rather than restricting ourselves to the simple pair case, though this would require a different framework (e.g. the Johansen test) rather than a direct extension of Engle-Granger.
- An optimisation exercise on the window size parameters could help us more deeply tackle the question of: how long do these relationships last?
- As mentioned above, we used log price for the majority of this project due to the multiplicative nature of stock returns over many years, however over shorter time periods (intra-day) this may be negligible and returns may be modelled better as additive, meaning that we may be able to use raw price. As mentioned in [notebook 2](notebooks/02_baseline_cointegration.ipynb), this actually gives us a natural portfolio whose value is a stationary series, making it easier to trade.
