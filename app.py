import streamlit as st
import pandas as pd
import plotly.express as px


class DataManager:

    def __init__(self):
        self.data = None

    def load_data(self, uploaded_file):
        self.data = pd.read_csv(uploaded_file)
        return self.data

    def statistics(self):
        return self.data.describe()


class ReportManager:

    def save_report(self, stats):
        stats.to_csv("analysis_report.csv")
        return "analysis_report.csv"


st.title("Інтерактивна панель аналізу даних")

uploaded_file = st.file_uploader(
    "Оберіть CSV-файл",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        manager = DataManager()

        df = manager.load_data(uploaded_file)

        st.subheader("Дані")
        st.dataframe(df)

        st.subheader("Статистика")

        stats = manager.statistics()

        st.dataframe(stats)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:

            selected_column = st.selectbox(
                "Оберіть стовпець",
                numeric_columns
            )

            fig = px.histogram(
                df,
                x=selected_column,
                title=f"Розподіл {selected_column}"
            )

            st.plotly_chart(fig)

        report = ReportManager()

        report_file = report.save_report(stats)

        st.success(
            f"Звіт збережено: {report_file}"
        )

    except FileNotFoundError:
        st.error(
            "Файл не знайдено."
        )

    except pd.errors.ParserError:
        st.error(
            "Помилка формату CSV."
        )

    except Exception as e:
        st.error(
            f"Помилка: {e}"
        )

else:
    st.info(
        "Завантажте CSV-файл для аналізу."
    )