import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt

# --- загрузка и подготовка ---
def load_data(data):
    df = pd.DataFrame(data, columns=["Время", "Пол", "Оценка"])

    df["Оценка"] = df["Оценка"].str.replace(",", ".").astype(float)

    today = dt.date.today()
    df["Время"] = pd.to_datetime(df["Время"], format="%H:%M").apply(
        lambda t: dt.datetime.combine(today, t.time())
    )

    df["Период"] = df["Время"].apply(
        lambda x: "Вечер" if x.hour >= 17 else "День"
    )

    return df


# --- универсальный Welch тест ---
def welch_test(sample1, sample2, alternative="greater"):
    mean1 = np.mean(sample1)
    mean2 = np.mean(sample2)
    diff = mean1 - mean2

    t_stat, p_value = stats.ttest_ind(
        sample1,
        sample2,
        equal_var=False,
        alternative=alternative
    )

    return {
        "mean1": mean1,
        "mean2": mean2,
        "diff": diff,
        "t_stat": t_stat,
        "p_value": p_value
    }


# --- гипотезы ---
def test_gender(df):
    boys = df[df["Пол"] == "М"]["Оценка"]
    girls = df[df["Пол"] == "Ж"]["Оценка"]
    return welch_test(boys, girls)


def test_period(df):
    evening = df[df["Период"] == "Вечер"]["Оценка"]
    day = df[df["Период"] == "День"]["Оценка"]
    return welch_test(evening, day)