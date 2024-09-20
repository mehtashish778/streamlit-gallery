import json
from streamlit_elements import nivo, mui
from .dashboard import Dashboard
import pandas as pd
from io import StringIO


class LineGraph(Dashboard.Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "#FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, csv_file, labels, graph_title):
        # labels is a dictionary containing keys as labels and values as column names in the CSV file
        try:
            data = pd.read_csv(StringIO(csv_file))  # Use StringIO directly
        except Exception as e:
            raise Exception("No data available: " + str(e))

        label_list = list(labels.keys())
        label_values = list(labels.values())

        if len(label_list) != len(label_values):
            raise Exception("Number of labels and values must be equal")

        # Prepare the final data for Nivo-compatible format
        final_data = []
        for i in range(len(label_list)):
            # Convert to datetime
            data[label_values[i]] = pd.to_datetime(data[label_values[i]])

            # Group data by date and count comments
            grouped_data = data.groupby(data[label_values[i]].dt.date)[label_values[i]].count().reset_index(name=label_list[i])
            
            # Append the formatted data to final_data
            final_data.append({
                "id": label_list[i],
                "data": [{"x": str(row[label_values[i]]), "y": row[label_list[i]]} for _, row in grouped_data.iterrows()]
            })

        # Using mui elements to create the dashboard
        with mui.Paper(
                key=self._key,
                sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                elevation=1
        ):
            # Title bar with mui elements
            with self.title_bar():
                mui.icon.Timeline()
                mui.Typography(f"{graph_title}", sx={"flex": 1, "fontSize": 18, "fontWeight": 600})

            # Box container for the line chart
            with mui.Box(sx={"flex": 1, "minHeight": 400}):
                nivo.Line(
                    data=final_data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    margin={"top": 50, "right": 110, "bottom": 50, "left": 60},
                    xScale={"type": "point"},
                    yScale={"type": "linear", "min": "auto", "max": "auto", "stacked": False, "reverse": False},
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        "orient": "bottom",
                        "legend": "Date",
                        "legendOffset": 36,
                        "legendPosition": "middle"
                    },
                    axisLeft={
                        "orient": "left",
                        "legend": "Number of Comments",
                        "legendOffset": -40,
                        "legendPosition": "middle"
                    },
                    colors={"scheme": "nivo"},
                    pointSize=10,
                    pointColor={"theme": "background"},
                    pointBorderWidth=2,
                    pointBorderColor={"from": "serieColor"},
                    pointLabelYOffset=-12,
                    useMesh=True,
                    legends=[
                        {
                            "anchor": "bottom-right",
                            "direction": "column",
                            "justify": False,
                            "translateX": 100,
                            "translateY": 0,
                            "itemsSpacing": 0,
                            "itemDirection": "left-to-right",
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemOpacity": 0.75,
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "symbolBorderColor": "rgba(0, 0, 0, .5)",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemBackground": "rgba(0, 0, 0, .03)",
                                        "itemOpacity": 1
                                    }
                                }
                            ]
                        }
                    ]
                )
