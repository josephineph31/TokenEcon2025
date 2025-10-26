import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
df = pd.read_csv("team_token.csv")
df['Net_Tokens'] = df['Tokens_Earned'] - df['Tokens_Delegated'] + df['Tokens_Received']
numeric_cols = ['Tokens_Earned', 'Tokens_Delegated', 'Tokens_Received', 'Net_Tokens']
df[numeric_cols] = df[numeric_cols].astype(int)
st.set_page_config(layout="wide", page_title="Weekly Task Tracker")
st.title("Team Weekly Task Tracker")
st.markdown("Track **Tokens Earned**, **Delegations**, and **Net Tokens** per team member over time.")
with st.sidebar:
    st.header("Navigation Browser")
    unique_weeks = sorted(df['Week'].unique())
    selected_weeks = st.multiselect("Select Week(s):", unique_weeks, default=unique_weeks)
    unique_members = sorted(df['Member'].unique())
    selected_members = st.multiselect("Select Member(s):", unique_members, default=unique_members)
df_filtered = df[
    df['Week'].isin(selected_weeks) & df['Member'].isin(selected_members)
]
st.header("1. Consolidated Weekly Summary")
if df_filtered.empty:
    st.warning("No data matches the selected filters.")
else:
    summary_df = df_filtered.groupby("Member").agg(
        Total_Earned=('Tokens_Earned', 'sum'),
        Total_Delegated=('Tokens_Delegated', 'sum'),
        Total_Received=('Tokens_Received', 'sum'),
        Net_Tokens=('Net_Tokens', 'sum')
    ).reset_index().sort_values(by='Net_Tokens', ascending=False)
    summary_numeric_cols = ['Total_Earned', 'Total_Delegated', 'Total_Received', 'Net_Tokens']
    summary_df[summary_numeric_cols] = summary_df[summary_numeric_cols].astype(int)

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Net_Tokens": st.column_config.ProgressColumn(
                "Net Tokens",
                help="Earned - Delegated + Received",
                format="%d",
                min_value=0,
                max_value=int(summary_df['Net_Tokens'].max())
            )
        }
    )
    st.header("2. Tokens by Member (Chart)")
    fig = px.bar(
        summary_df,
        x="Member",
        y="Total_Earned",
        title="Total Tokens Earned by Member",
        color="Member",
        text="Total_Earned",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        template="plotly_dark"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
st.header("3. Detailed Task Log")
st.dataframe(
    df_filtered.sort_values(by=['Week', 'Member', 'Task']),
    use_container_width=True
)
