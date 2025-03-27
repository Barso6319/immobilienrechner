import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Immobilienrechner V6", layout="centered")

# ----------------------------- #
# Funktion: Monatliche Annuität berechnen
# ----------------------------- #
def berechne_annuitaet_monatlich(kreditsumme, sollzins_prozent, laufzeit_jahre):
    i = sollzins_prozent / 100 / 12  # Monatszins
    n = laufzeit_jahre * 12          # Anzahl Monate

    if i == 0:
        return kreditsumme / n

    faktor = (i * (1 + i) ** n) / ((1 + i) ** n - 1)
    return kreditsumme * faktor

# ----------------------------- #
# Funktion: Monatlicher Tilgungsplan
# ----------------------------- #
def tilgungsplan_monatlich(kreditsumme, sollzins, laufzeit, sondertilgung_jahr):
    monatsrate = berechne_annuitaet_monatlich(kreditsumme, sollzins, laufzeit)
    restschuld = kreditsumme
    plan = []

    for monat in range(1, laufzeit * 12 + 1):
        jahr = (monat - 1) // 12 + 1
        zins = restschuld * (sollzins / 100 / 12)
        tilgung = monatsrate - zins

        # Sondertilgung immer im Dezember
        if monat % 12 == 0 and restschuld > 0:
            tilgung += sondertilgung_jahr

        restschuld = max(0, restschuld - tilgung)

        plan.append({
            "Monat": monat,
            "Jahr": jahr,
            "Zinszahlung": round(zins, 2),
            "Tilgung": round(tilgung, 2),
            "Gesamtrate": round(monatsrate + (sondertilgung_jahr if monat % 12 == 0 else 0), 2),
            "Restschuld": round(restschuld, 2),
            "Sondertilgung": sondertilgung_jahr if monat % 12 == 0 else 0
        })

        if restschuld <= 0:
            break

    return pd.DataFrame(plan)

# ----------------------------- #
# Eingabebereich
# ----------------------------- #
st.title("🏡 Immobilienfinanzierungs-Rechner – Version 6 (monatlich genau)")

col1, col2, col3 = st.columns(3)

with col1:
    kaufpreis = st.number_input("Kaufpreis (€)", 50000, 2000000, 400000, 10000)
    eigenkapital = st.number_input("Eigenkapital (€)", 0, 2000000, 80000, 10000)
    nebenkosten_prozent = st.number_input("Nebenkosten (%)", 0.0, 20.0, 10.0, 0.5)

with col2:
    sollzins = st.number_input("Sollzins (% p.a.)", 0.1, 10.0, 3.0, 0.1)
    laufzeit = st.number_input("Laufzeit (Jahre)", 5, 40, 30, 1)
    zinsbindung = st.number_input("Zinsbindung (Jahre)", 1, 30, 10, 1)

with col3:
    sondertilgung = st.number_input("Jährliche Sondertilgung (€)", 0, 50000, 1000, 500)

# ----------------------------- #
# Berechnung starten
# ----------------------------- #
if st.button("💰 Finanzierung berechnen"):
    nebenskosten = kaufpreis * (nebenkosten_prozent / 100)
    gesamtkosten = kaufpreis + nebenskosten
    kreditsumme = gesamtkosten - eigenkapital

    df_monatlich = tilgungsplan_monatlich(kreditsumme, sollzins, laufzeit, sondertilgung)
    laufzeit_effektiv = df_monatlich["Monat"].max() // 12 + 1
    zinsbindungen = math.ceil(laufzeit_effektiv / zinsbindung)

    # ----------------------------- #
    # Zusammenfassung pro Jahr für Grafik
    # ----------------------------- #
    df_jahr = df_monatlich.groupby("Jahr").agg({
        "Zinszahlung": "sum",
        "Tilgung": "sum"
    }).reset_index()

    # ----------------------------- #
    # Ergebnisübersicht
    # ----------------------------- #
    st.subheader("📊 Ergebnisübersicht")
    st.markdown(f"**Gesamtkosten:** {gesamtkosten:,.2f} €")
    st.markdown(f"**Kreditsumme:** {kreditsumme:,.2f} €")
    st.markdown(f"**Voraussichtliche Laufzeit:** {laufzeit_effektiv} Jahre")
    st.markdown(f"**Zinsbindungsphasen:** {zinsbindungen} x {zinsbindung} Jahre")

    # ----------------------------- #
    # Grafik
    # ----------------------------- #
    st.subheader("📈 Jährlicher Verlauf")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_jahr["Jahr"], df_jahr["Zinszahlung"], label="Zins", color="red", alpha=0.6)
    ax.bar(df_jahr["Jahr"], df_jahr["Tilgung"], bottom=df_jahr["Zinszahlung"], label="Tilgung", color="green", alpha=0.8)
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Zahlung in €")
    ax.set_title("Zins- und Tilgungsverlauf pro Jahr")
    ax.legend()
    st.pyplot(fig)

    # ----------------------------- #
    # Monatliche Tabelle
    # ----------------------------- #
    st.subheader("📋 Monatlicher Tilgungsplan")
    st.dataframe(df_monatlich.style.format({
        "Zinszahlung": "{:,.2f}",
        "Tilgung": "{:,.2f}",
        "Gesamtrate": "{:,.2f}",
        "Restschuld": "{:,.2f}",
        "Sondertilgung": "{:,.2f}"
    }))

    # ----------------------------- #
    # Download
    # ----------------------------- #
    csv = df_monatlich.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Tilgungsplan als CSV herunterladen",
        data=csv,
        file_name="tilgungsplan_monatlich.csv",
        mime="text/csv"
    )

else:
    st.info("Bitte gib deine Werte ein und klicke auf **💰 Finanzierung berechnen**.")
