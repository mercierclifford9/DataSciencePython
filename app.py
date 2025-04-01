import streamlit as st
import pandas as pd




df = pd.DataFrame({'Nom': ['Alice', 'Bob', 'Charlie'], 'Âge': [25, 30, 35]})
st.dataframe(df)
st.table(df)

nom = st.text_input("Votre nom")
age = st.number_input("Votre âge", min_value=0, max_value=100)
if st.button("Valider"):
    st.write(f"Bonjour {nom}, vous avez {age} ans.")


# st.title("Mon Titre")
# st.header("Un Sous-titre")
# st.subheader("Un plus petit sous-titre")
# st.text("Texte simple")
# st.markdown("**Texte en gras** et *italique*")


# Pour ajouter des graphique 
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)


# pour televerser un fichier 
uploaded_file = st.file_uploader("Choisissez un fichier", type=["csv", "txt"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
