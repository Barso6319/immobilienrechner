import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Immobilienrechner V3", layout="centered")

# ----------------------------- #
# Funktion: Tilgungsplan berechnen
# ----------------------------- #
def tilgungsplan_erstellen(kreditsumme, sollzins, tilgung_start, tilgung_neu, wechseljahr, zinsbindung):
    jahresrate = lambda restschuld, tilgung: restschuld * (sollzins + tilgung) / 100
    plan = []
    restschuld = kreditsumme
    jahr = 1

    while restschuld > 0:
        aktueller_tilgungswert = tilgung_start if jahr < wechseljahr else tilgung_neu
        rate = jahresrate(restschuld, aktueller_tilgungswert)
        zins = restschuld * (sollzins / 100)
        tilgung = rate - zins
        restschuld = max(0, restschuld - tilgung)

        plan.append({
            "Jahr": jahr,
            "Zinszahlung": round(zins, 2),
            "Tilgung": round(tilgung, 2),
            "Restschuld": round(restschuld, 2),
            "Tilgungssatz": aktueller_tilgungswert
        })
        jahr += 1

    return plan

# ----------------------------- #
# Layout oben: Eingabefelder
# ----------------------------- #

st.title("🏡 Immobilienfinanzierungs-Rechner – Version 3")
st.markdown("Diese Version enthält Tilgungswechsel & verbessertes Layout.")

col1, col2, col3 = st.columns(3)

with col1:
    kaufpreis = st.number_input("Kaufpreis (€)", 50000, 2000000, 400000, 10000)
    eigenkapital = st.number_input("Eigenkapital (€)", 0, 2000000, 80000, 10000)
    nebenkosten_prozent = st.number_input("Nebenkosten (%)", 0.0, 20.0, 10.0, 0.5)

with col2:
    sollzins = st.number_input("Sollzins (% p.a.)", 0.1, 10.0, 3.0, 0.1)
    tilgungssatz = st.number_input("Starttilgung (% p.a.)", 0.5, 10.0, 2.0, 0.1)
    zinsbindung = st.number_input("Zinsbindung (Jahre)", 1, 30, 10, 1)

with col3:
    wechseljahr = st.number_input("Tilgungswechsel ab Jahr", 2, 50, 11, 1)
    neue_tilgung = st.number_input("Neue Tilgung (% p.a.)", 0.5, 10.0, 3.5, 0.1)

# ----------------------------- #
# Berechnung starten
# ----------------------------- #
if st.button("💰 Finanzierung berechnen"):
    # Basiskalkulation
    nebenskosten = kaufpreis * (nebenkosten_prozent / 100)
    gesamtkosten = kaufpreis + nebenskosten
    kreditsumme = gesamtkosten - eigenkapital

    # Tilgungsplan berechnen
    plan = tilgungsplan_erstellen(kreditsumme, sollzins, tilgungssatz, neue_tilgung, wechseljahr, zinsbindung)
    df = pd.DataFrame(plan)

    laufzeit = len(df)
    zinsbindungen = math.ceil(laufzeit / zinsbindung)

    # ----------------------------- #
    # Ergebnisübersicht
    # ----------------------------- #
    st.subheader("📊 Ergebnisübersicht")
    st.markdown(f"**Gesamtkosten:** {gesamtkosten:,.2f} €")
    st.markdown(f"**Kreditsumme:** {kreditsumme:,.2f} €")
    st.markdown(f"**Voraussichtliche Laufzeit:** {laufzeit} Jahre")
    st.markdown(f"**Zinsbindungsphasen:** {zinsbindungen} x {zinsbindung} Jahre")

    # ----------------------------- #
    # Grafik: Tilgung vs. Zins
    # ----------------------------- #
    st.subheader("📈 Tilgungsverlauf")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["Jahr"], df["Zinszahlung"], label="Zins", color="red", alpha=0.6)
    ax.bar(df["Jahr"], df["Tilgung"], bottom=df["Zinszahlung"], label="Tilgung", color="green", alpha=0.8)
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Zahlung in €")
    ax.set_title("Zins- und Tilgungsverlauf")
    ax.legend()
    st.pyplot(fig)

    # ----------------------------- #
    # Tabelle: Tilgungsplan
    # ----------------------------- #
    st.subheader("📋 Tilgungsplan (Tabelle)")
    st.dataframe(df.style.format({
        "Zinszahlung": "{:,.2f}",
        "Tilgung": "{:,.2f}",
        "Restschuld": "{:,.2f}",
        "Tilgungssatz": "{:,.2f}"
    }))
else:
    st.info("Bitte gib alle Werte ein und klicke auf **💰 Finanzierung berechnen**.")
