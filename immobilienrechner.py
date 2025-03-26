import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Immobilienrechner V2", layout="centered")

# ----------------------------- #
# Berechnung der Tilgung & Zins
# ----------------------------- #
def tilgungsplan_erstellen(kreditsumme, sollzins, tilgungssatz, zinsbindung):
    jahresrate = kreditsumme * (sollzins + tilgungssatz) / 100
    plan = []
    restschuld = kreditsumme
    jahr = 1

    while restschuld > 0:
        zins = restschuld * (sollzins / 100)
        tilgung = jahresrate - zins
        restschuld = max(0, restschuld - tilgung)

        plan.append({
            "Jahr": jahr,
            "Zinszahlung": round(zins, 2),
            "Tilgung": round(tilgung, 2),
            "Restschuld": round(restschuld, 2)
        })
        jahr += 1

    return plan

# ------------------------ #
# Eingabebereich
# ------------------------ #
st.title("🏡 Immobilienfinanzierung – Version 2")

st.sidebar.header("📥 Eingaben")

kaufpreis = st.sidebar.number_input("Kaufpreis (€)", 50000, 2000000, 400000, 10000)
eigenkapital = st.sidebar.number_input("Eigenkapital (€)", 0, 2000000, 80000, 10000)
sollzins = st.sidebar.number_input("Sollzins (% p.a.)", 0.1, 10.0, 3.0, 0.1)
tilgungssatz = st.sidebar.number_input("Anfängliche Tilgung (% p.a.)", 0.5, 10.0, 2.0, 0.1)
nebenkosten_prozent = st.sidebar.number_input("Nebenkosten (% vom Kaufpreis)", 0.0, 20.0, 10.0, 0.5)
zinsbindung = st.sidebar.number_input("Zinsbindung (Jahre)", 1, 30, 10, 1)

# ------------------------ #
# Berechnung und Anzeige
# ------------------------ #
if st.sidebar.button("💰 Finanzierung berechnen"):
    # Grundrechnungen
    nebenskosten = kaufpreis * (nebenkosten_prozent / 100)
    gesamtkosten = kaufpreis + nebenskosten
    kreditsumme = gesamtkosten - eigenkapital

    plan = tilgungsplan_erstellen(kreditsumme, sollzins, tilgungssatz, zinsbindung)
    df = pd.DataFrame(plan)

    # Gesamtlaufzeit
    laufzeit = len(df)
    zinsbindungsphasen = math.ceil(laufzeit / zinsbindung)

    # Ergebnisse anzeigen
    st.subheader("📊 Ergebnisübersicht")
    st.markdown(f"**Gesamtkosten:** {gesamtkosten:,.2f} €")
    st.markdown(f"**Kreditsumme:** {kreditsumme:,.2f} €")
    st.markdown(f"**Voraussichtliche Laufzeit:** {laufzeit} Jahre")
    st.markdown(f"**Zinsbindungsphasen benötigt:** {zinsbindungsphasen} x {zinsbindung} Jahre")

    # Chart erstellen
    st.subheader("📈 Tilgungsverlauf")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["Jahr"], df["Zinszahlung"], label="Zins", alpha=0.6)
    ax.bar(df["Jahr"], df["Tilgung"], bottom=df["Zinszahlung"], label="Tilgung", alpha=0.8)
    ax.set_xlabel("Jahre")
    ax.set_ylabel("Zahlung in €")
    ax.set_title("Zins- und Tilgungsverlauf pro Jahr")
    ax.legend()
    st.pyplot(fig)

    # Tabelle anzeigen
    st.subheader("📋 Tilgungsplan (Tabelle)")
    st.dataframe(df.style.format({"Zinszahlung": "{:,.2f}", "Tilgung": "{:,.2f}", "Restschuld": "{:,.2f}"}))

else:
    st.info("Bitte gib deine Werte ein und klicke auf **💰 Finanzierung berechnen**.")


