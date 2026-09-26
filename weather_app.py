import streamlit as st## creates the web dashborsda
import pandas as pd# loading the weather data
import plotly.express as px# create interactive charts


##I used Pandas to read the CSV file, 
# manipulate the weather data, create new columns, 
# filter records, 
# and calculate statistics such as averages and 
# minimum and maximum temperatures.
# 

#Page Creation


st.set_page_config(
    page_title="Toronto Weather 2012",
    page_icon="🌦️",
    layout="wide"
)
#controls how the Streamlit page looks like


# Data Loading


@st.cache_data# defines the function load_data()
def load_data():
    df = pd.read_csv(
        r"C:\Users\PatrickNjuguna\Desktop\py_data\weather_2012.csv"
    )
#basically it tells the progra
    # Converting  Date/Time to datetime
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])

    # Creating columns that are usefull 
    df["Month"] = df["Date/Time"].dt.month
    df["Month Name"] = df["Date/Time"].dt.strftime("%B")
    df["Day"] = df["Date/Time"].dt.day

    return df


df = load_data()


##Creating the tittle for the page


st.title("Toronto Weather 2012")

st.subheader(
    "An interactive dashboard on Toronto weather data"
)



## Creating side bar filters


st.sidebar.header("Weather Filters")

# Month filtering
month = st.sidebar.slider(
    "Select Month",
    min_value=1,
    max_value=12,
    value=1,
    step=1
)

# Measurement filtering
metric = st.sidebar.selectbox(
    "Select Measurement",
    ["Temperature", "Humidity"]
)

# Weather condition filtering
weather_options = ["All"] + sorted(df["Weather"].dropna().unique().tolist())

weather = st.sidebar.selectbox(
    "Select Weather Condition",
    weather_options
)


##Filtering the data

filtered_df = df[df["Month"] == month].copy()

if weather != "All":
    filtered_df = filtered_df[
        filtered_df["Weather"] == weather
    ]

# MONTH NAME


month_name = pd.to_datetime(
    str(month),
    format="%m"
).strftime("%B")



# FILTER INFORMATION

st.info(
    f"{month_name}"
    + (
        f" and **{weather}** weather conditions."
        if weather != "All"
        else "."
    )
)



# KPI METRICS


st.header("📊 Weather Summary")


if not filtered_df.empty:

    avg_temp = filtered_df["Temp (C)"].mean()
    max_temp = filtered_df["Temp (C)"].max()
    min_temp = filtered_df["Temp (C)"].min()
    avg_humidity = filtered_df["Rel Hum (%)"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡️ Average Temperature",
        f"{avg_temp:.1f} °C"
    )

    col2.metric(
        "🔥 Maximum Temperature",
        f"{max_temp:.1f} °C"
    )

    col3.metric(
        "❄️ Minimum Temperature",
        f"{min_temp:.1f} °C"
    )

    col4.metric(
        "💧 Average Humidity",
        f"{avg_humidity:.1f}%"
    )

else:

    st.warning(
        "No weather records match the selected filters."
    )



# MAIN MEASUREMENT CHART


st.header("📈 Weather Over Time")


if not filtered_df.empty:

    if metric == "Temperature":

        fig = px.line(
            filtered_df,
            x="Date/Time",
            y="Temp (C)",
            title=f"Temperature During {month_name} 2012",
            markers=True,
            labels={
                "Date/Time": "Date and Time",
                "Temp (C)": "Temperature (°C)"
            }
        )

        fig.update_layout(
            hovermode="x unified",
            template="plotly_white"
        )

    else:

        fig = px.line(
            filtered_df,
            x="Date/Time",
            y="Rel Hum (%)",
            title=f"Relative Humidity During {month_name} 2012",
            markers=True,
            labels={
                "Date/Time": "Date and Time",
                "Rel Hum (%)": "Relative Humidity (%)"
            }
        )

        fig.update_layout(
            hovermode="x unified",
            template="plotly_white"
        )

    st.plotly_chart(
        fig,
        width="content"
    )



# TEMPERATURE AND HUMIDITY


st.header("🌡️ Temperature vs 💧 Humidity")


if not filtered_df.empty:

    fig_scatter = px.scatter(
        filtered_df,
        x="Temp (C)",
        y="Rel Hum (%)",
        color="Weather",
        title="Temperature vs Relative Humidity",
        labels={
            "Temp (C)": "Temperature (°C)",
            "Rel Hum (%)": "Relative Humidity (%)",
            "Weather": "Weather Condition"
        },
        hover_data=["Date/Time"]
    )

    fig_scatter.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_scatter,
       width ="content"
    )



# WEATHER CONDITION ANALYSIS


st.header("🌤️ Average Temperature by Weather Condition")


avg_temp = (
    df.groupby("Weather")["Temp (C)"]
    .mean()
    .reset_index()
    .sort_values("Temp (C)")
)


fig_weather = px.bar(
    avg_temp,
    x="Weather",
    y="Temp (C)",
    title="Average Temperature by Weather Condition",
    labels={
        "Weather": "Weather Condition",
        "Temp (C)": "Average Temperature (°C)"
    }
)

fig_weather.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_weather,
    width ="content"
)



# HUMIDITY DISTRIBUTION


st.header("💧 Humidity Distribution")


if not filtered_df.empty:

    fig_humidity = px.histogram(
        filtered_df,
        x="Rel Hum (%)",
        nbins=20,
        title=f"Relative Humidity Distribution - {month_name}",
        labels={
            "Rel Hum (%)": "Relative Humidity (%)"
        }
    )

    fig_humidity.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_humidity,
        width="content")


# TEMPERATURE DISTRIBUTION


st.header("🌡️ Temperature Distribution")


if not filtered_df.empty:

    fig_temperature = px.histogram(
        filtered_df,
        x="Temp (C)",
        nbins=30,
        title=f"Temperature Distribution - {month_name}",
        labels={
            "Temp (C)": "Temperature (°C)"
        }
    )

    fig_temperature.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_temperature,
       width = "content"
    )



# DATA TABLE


st.header("📋 Weather Records")

st.write(
    f"Showing **{len(filtered_df):,}** records."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# WEATHER CONDITION PIE CHART
st.header("🥧 Weather Condition Distribution")

weather_counts = (
    filtered_df["Weather"]
    .value_counts()
    .reset_index()
)

weather_counts.columns = ["Weather", "Count"]

fig_pie = px.pie(
    weather_counts,
    names="Weather",
    values="Count",
    title=f"Weather Conditions - {month_name} 2012",
    hole=0.3,
    height=650
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont_size=16
)

fig_pie.update_layout(
    title_font_size=24,
    margin=dict(t=80, l=20, r=20, b=20)
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Toronto Weather 2012 Dashboard | Built with Python, "
    "Pandas, Plotly and Streamlit, By Patrick Macharia Njuguna"
)