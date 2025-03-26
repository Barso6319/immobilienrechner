import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from io import BytesIO

st.set_page_config(page_title="Immobilienrechner V5", layout="centered")

# ----------------------------- #
# Funktion: Exakte Annuität berechnen
# ----------------------------- #
def berechne_annuitaet(kreditsumme, sollzins_prozent, laufzeit_jahre):
    i = sollzins_prozent / 100 / 12  # Monatszins
    n = laufzeit_jahre * 12          # Anzahl Monate

    if i == 0:  # Sonderfall zinsfrei
        return kreditsumme / n * 12  # jährliche Rate

    faktor = (i * (1 + i) ** n) / ((1 + i) ** n - 1)
    annuitaet_monatlich = kreditsumme * faktor
    return annuitaet_monatlich * 12  # jährliche Annuität

# ----------------------------- #
# Tilgungsplan mit exakter Annuität
# ----------------------------- #
def tilgungsplan_erstellen(kreditsumme, sollzins, laufzeit, sondertilgung):
    jahr = 1
    restschuld = kreditsumme
    plan = []
    annuitaet_jahr = berechne_annuitaet(kreditsumme, sollzins, laufzeit)

    while restschuld > 0 and jahr <= laufzeit:
        zins = restschuld * (sollzins / 100)
        tilgung = annuitaet_jahr - zins + sondertilgung
        restschuld = max(0, restschuld - tilgung)

        plan.append({
            "Jahr": jahr,
            "Zinszahlung": round(zins, 2),
            "Tilgung (inkl. Sondertilgung)": round(tilgung, 2),
            "Restschuld": round(restschuld, 2),
            "Annuität": round(annuitaet_jahr, 2),
            "Sondertilgung": sondertilgung
        })

        jahr += 1

    return plan

# ----------------------------- #
# Layout oben: Eingabefelder
# ----------------------------- #

st.title("🏡 Immobilienfinanzierungs-Rechner – Version 5 (exakte Methode)")

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

    plan = tilgungsplan_erstellen(kreditsumme, sollzins, laufzeit, sondertilgung)
    df = pd.DataFrame(plan)
    laufzeit_effektiv = len(df)
    zinsbindungen = math.ceil(laufzeit_effektiv / zinsbindung)

    # ----------------------------- #
    # Ergebnisübersicht
    # ----------------------------- #
    st.subheader("📊 Ergebnisübersicht")
    st.markdown(f"**Gesamtkosten:** {gesamtkosten:,.2f} €")
    st.markdown(f"**Kreditsumme:** {kreditsumme:,.2f} €")
    st.markdown(f"**Voraussichtliche Laufzeit:** {laufzeit_effektiv} Jahre")
    st.markdown(f"**Zinsbindungsphasen:** {zinsbindungen} x {zinsbindung} Jahre")

    # ----------------------------- #
    # Grafik: Tilgung vs. Zins
    # ----------------------------- #
    st.subheader("📈 Tilgungsverlauf")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["Jahr"], df["Zinszahlung"], label="Zins", color="red", alpha=0.6)
    ax.bar(df["Jahr"], df["Tilgung (inkl. Sondertilgung)"], bottom=df["Zinszahlung"], label="Tilgung", color="green", alpha=0.8)
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
        "Tilgung (inkl. Sondertilgung)": "{:,.2f}",
        "Restschuld": "{:,.2f}",
        "Annuität": "{:,.2f}",
        "Sondertilgung": "{:,.2f}"
    }))

    # ----------------------------- #
    # Download als Excel (CSV)
    # ----------------------------- #
    st.subheader("📥 Tilgungsplan herunterladen")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 CSV-Datei herunterladen",
        data=csv,
        file_name="tilgungsplan.csv",
        mime="text/csv"
    )

else:
    st.info("Bitte gib alle Werte ein und klicke auf **💰 Finanzierung berechnen**.")

else:
    st.info("Bitte gib alle Werte ein und klicke auf **💰 Finanzierung berechnen**.")

