import streamlit as st
import matplotlib.pyplot as plt

from backend import load_data, test_gender, test_period
from data import DATA

# --- стиль 💖 ---
st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {background-color: #fff0f6;}
h1, h2, h3 {color: #d63384;}
</style>
""", unsafe_allow_html=True)

st.title("💖 Анализ оценок студентов за экзамен по ИПР")

df = load_data(DATA)

# --- таблица ---
st.subheader("📋 Данные")
st.dataframe(df)

# --- распределения ---
st.subheader("📊 Распределения")

col1, col2 = st.columns(2)

boys = df[df["Пол"] == "М"]["Оценка"]
girls = df[df["Пол"] == "Ж"]["Оценка"]

with col1:
    fig, ax = plt.subplots()
    ax.hist(boys, bins=8, alpha=0.7, label="Мальчики")
    ax.hist(girls, bins=8, alpha=0.7, label="Девочки")
    ax.legend()
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    df.boxplot(column="Оценка", by="Пол", ax=ax2)
    plt.suptitle("")
    st.pyplot(fig2)

# --- гипотеза 1 ---
st.subheader("🧠 Гипотеза 1: у мальчиков оценки выше")

res1 = test_gender(df)

st.write(f"Среднее (М): {res1['mean1']:.2f}")
st.write(f"Среднее (Ж): {res1['mean2']:.2f}")
st.write(f"Разница: {res1['diff']:.2f}")
st.write(f"t = {res1['t_stat']:.3f}")
st.write(f"p-value = {res1['p_value']:.5f}")

st.markdown("""
**Обоснование:**  
Используется Welch t-test, так как выборки могут иметь разные дисперсии и размеры.
""")

if res1["p_value"] < 0.05:
    st.success("💖 Гипотеза подтверждается")
else:
    st.error("💔 Нет значимого различия")

# --- гипотеза 2 ---
st.subheader("🌙 Гипотеза 2: вечером оценки выше")

res2 = test_period(df)

st.write(f"Среднее (вечер): {res2['mean1']:.2f}")
st.write(f"Среднее (день): {res2['mean2']:.2f}")
st.write(f"Разница: {res2['diff']:.2f}")
st.write(f"t = {res2['t_stat']:.3f}")
st.write(f"p-value = {res2['p_value']:.5f}")

if res2["p_value"] < 0.05:
    st.success("🌸 Есть значимый эффект")
else:
    st.warning("🌧 Эффект не подтверждён статистически")