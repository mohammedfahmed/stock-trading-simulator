
import altair as alt


def visualize_backtest_results(results):

    # Ensure the index is part of the DataFrame
    if not 'Date' in results.columns:
        results = results.reset_index(names='Date')

    # Prepare data for cumulative returns chart
    cumulative_returns_data = results.melt(
        id_vars=['Date'],
        value_vars=['Cumulative_Returns', 'Strategy_Cumulative_Returns'],
        var_name='Type',
        value_name='Value'
    )

    cumulative_returns_chart = (
        alt.Chart(cumulative_returns_data, title="Cumulative Returns")
        .mark_line()
        .encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('Value:Q', title='Cumulative Returns'),
            color=alt.Color('Type:N', title='Series', scale=alt.Scale(scheme='tableau10'))
        )
    )

    # Prepare data for equity curve chart
    equity_curve_chart = (
        alt.Chart(results, title="Equity Curve")
        .mark_line(color='green')
        .encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('Portfolio_Value:Q', title='Portfolio Value')
        )
    )

    # Combine charts vertically
    final_chart = alt.vconcat(cumulative_returns_chart, equity_curve_chart)

    return final_chart
