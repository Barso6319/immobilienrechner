import streamlit as st

# Seiteneinstellungen
st.set_page_config(page_title="Immobilienrechner", layout="centered")

# 💡 Berechnungsfunktion
def berechne_immobilienfinanzierung(kaufpreis, eigenkapital, sollzins, tilgungssatz, nebenkosten_prozent):
    nebenskosten = kaufpreis * (nebenkosten_prozent / 100)
    gesamtkosten = kaufpreis + nebenskosten
    kreditsumme = gesamtkosten - eigenkapital
    annuitaet = kreditsumme * (sollzins + tilgungssatz) / 100
    monatsrate = annuitaet / 12
    return gesamtkosten, kreditsumme, annuitaet, monatsrate

# 🧾 Titel & Eingaben
st.title("🏡 Immobilienfinanzierungs-Rechner")
st.sidebar.header("📥 Eingaben")

kaufpreis = st.sidebar.number_input("Kaufpreis der Immobilie (€)", min_value=50000, max_value=2000000, value=400000, step=10000)
eigenkapital = st.sidebar.number_input("Eigenkapital (€)", min_value=0, max_value=2000000, value=80000, step=10000)
sollzins = st.sidebar.number_input("Sollzins (% p.a.)", min_value=0.1, max_value=10.0, value=3.0, step=0.1)
tilgungssatz = st.sidebar.number_input("Anfängliche Tilgung (% p.a.)", min_value=0.5, max_value=10.0, value=2.0, step=0.1)
nebenkosten_prozent = st.sidebar.number_input("Nebenkosten (% vom Kaufpreis)", min_value=0.0, max_value=20.0, value=10.0, step=0.5)

# 🧮 Berechnung
if st.sidebar.button("💰 Finanzierung berechnen"):
    try:
        gesamtkosten, kreditsumme, annuitaet, monatsrate = berechne_immobilienfinanzierung(
            kaufpreis, eigenkapital, sollzins, tilgungssatz, nebenkosten_prozent
        )

        st.subheader("📊 Ergebnisse")
        st.success(f"**Gesamtkosten:** {gesamtkosten:,.2f} €")
        st.info(f"**Finanzierungsbedarf (Kredit):** {kreditsumme:,.2f} €")
        st.write(f"**Jährliche Rate (Annuität):** {annuitaet:,.2f} €")
        st.write(f"**Monatliche Rate:** {monatsrate:,.2f} €")

    except Exception as e:
        st.error(f"❌ Fehler bei der Berechnung: {e}")
else:
    st.info("Bitte gib alle Eingaben ein und klicke auf **💰 Finanzierung berechnen**.")


