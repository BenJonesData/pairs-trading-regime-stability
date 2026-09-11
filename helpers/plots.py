import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.api as sm


def model_fit_and_plots(df, col1, col2, col_description, return_results=True):
    fig, axes = plt.subplots(1, 2, figsize=(20, 5))
  
    axes[0].plot(df[col1], label=col1, color="blue")
    axes[0].plot(df[col2], label=col2, color="red")
    
    axes[0].legend()
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel(col_description)
    axes[0].set_title(f"{col_description} Over Time")

    axes[0].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[0].tick_params(axis='x', rotation=45)

    model_1_2 = sm.OLS(df[col2], sm.add_constant(df[col1]))
    results_1_2 = model_1_2.fit()

    model_2_1 = sm.OLS(df[col1], sm.add_constant(df[col2]))
    results_2_1 = model_2_1.fit()

    axes[1].plot(results_1_2.resid, label=f"{col1} regressed on {col2}")
    axes[1].plot(results_2_1.resid, label=f"{col2} regressed on {col1}")

    axes[1].legend()
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Residuals")    
    axes[1].set_title(f"OLS Residuals: {col1} vs {col2} (Both Regression Directions)")

    axes[1].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.show()

    if return_results:
        return {f"{col1} on {col2}": results_1_2, f"{col2} on {col1}": results_2_1}
    