import streamlit as st

st.set_page_config(page_title="Immobilienrechner", layout="centered")

def berechne_immobilienfinanzierung(kaufpreis, eigenkapital, sollzins, tilgungssatz, nebenskosten_prozent):
    nebenskosten = kaufpreis * (nebenkosten_prozent / 100)
    gesamtkosten = kaufpreis + nebenskosten
    kreditsumme = gesamtkosten - eigenkapital
    annuitaet = kreditsumme * (sollzins + tilgungssatz) / 100
    monatsrate = annuitaet / 12
    return gesamtkosten, kreditsumme, annuitaet, monatsrate

st.title("🏡 Immobilienfinanzierungs-Rechner")
st.sidebar.header("📥 Eingaben")

kaufpreis = st.sidebar.number_input("Kaufpreis (€)", 50000, 2000000, 400000, 10000)
eigenkapital = st.sidebar.number_input("Eigenkapital (€)", 0, 2000000, 80000, 10000)
sollzins = st.sidebar.number_input("Sollzins (% p.a.)", 0.1, 10.0, 3.0, 0.1)
tilgungssatz = st.sidebar.number_input("Tilgung (% p.a.)", 0.5, 10.0, 2.0, 0.1)
nebenkosten = st.sidebar.number_input("Nebenkosten (% vom Kaufpreis)", 0.0, 20.0, 10.0, 0.5)

if st.sidebar.button("💰 Finanzierung berechnen"):
    gesamt, kredit, jahr_rate, monat_rate = berechne_immobilienfinanzierung(
        kaufpreis, eigenkapital, sollzins, tilgungssatz, nebenkosten
    )
    st.subheader("📊 Ergebnisse")
    st.success(f"Gesamtkosten: {gesamt:,.2f} €")
    st.info(f"Kreditsumme: {kredit:,.2f} €")
    st.write(f"Jährliche Rate: {jahr_rate:,.2f} €")
    st.write(f"Monatliche Rate: {monat_rate:,.2f} €")
