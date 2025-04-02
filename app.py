import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import os
from utils.function_utils import data_cleaning, mean_median, update_data
from collections import Counter


def run ():
    st.title("Analyse des habitudes de consommation numérique")
    st.header("Bienvenue dans notre application d'analyse de données")

    st.text("Cette application vise a anayse les données recueillies a propos des habitudes de "
            "consomation numérique dans un formulaire creer avec google form ")

    # Recuperation du chemin vers le fichier de donnee 'data_digital_habits.csv'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(base_dir, "data", "data_digital_habits.csv")
    

    #Lecture du dataframe en local
    df = pd.read_csv(path_file, index_col=0)

    st.subheader("Nettoyage des donnnes (Data cleaning)")

    #creation du bouton pour mettre a jour les donnees
    if st.button("Cliquez pour mettre a jour les donnees"):
        update_data(df, path_file)


    st.text("Pour commencer nous allons vous presentez les donnees brut avant nettoyage")
    st.dataframe(df)


    df = data_cleaning(df) #Appel de notre foncion data_cleaning() declare dans function_utils.py
    st.text("Et voila les donnees apres nettoyage")
    st.dataframe(df)

    st.subheader("Analyse descriptive")

    st.markdown("##### <u>Moyennes et médianes du temps passé par activité</u>", unsafe_allow_html=True)

    #Calcul de la moyenne et de la mediane pour le temps passe dans les differentes actions
    calc_mean_median = mean_median(df) #Appel de notre foncion mean_median() declare dans function_utilis.py
    st.table(calc_mean_median) 
    st.write("*NB: L'unite de mesure est 'minute'*")

    st.subheader("Répartition des plateformes préférées par tranche dʼâge ou sexe")
    
    st.markdown("##### <u> Streaming </u>",unsafe_allow_html=True)
    option_1 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de streaming préférées", ("Sexe", "Age"), key="selectbox_1")

    if option_1 == 'Sexe':
        streaming_sexe = pd.crosstab(df['sexe'], df['streaming_pref'], normalize='index')*100

        st.table(streaming_sexe.rename(index={'F':'Feminin', 'M':'Masculin'}))
        st.markdown("*NB: L'unite de mesure est '%'*")
    else : 
        streaming_age = pd.crosstab(df['tranche_age'], df['streaming_pref'], normalize='index')*100
        
        st.table(streaming_age)
        st.markdown("*NB: L'unite de mesure est '%'*")

    st.markdown("##### <u> Reseaux Sociaux </u>",unsafe_allow_html=True)
    option_2 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de reseaux sociaux préférées", ("Sexe", "Age"), key="selectbox_2")
    
    if option_2 == 'Age':
        social_age = pd.crosstab(df['tranche_age'], df['reseau_social_pref'], normalize='index')*100

        st.table(social_age)
        st.markdown("*NB: L'unite de mesure est '%'*")
    else : 
        social_sexe = pd.crosstab(df['sexe'], df['reseau_social_pref'], normalize='index')*100
        
        st.table(social_sexe)
        st.markdown("*NB: L'unite de mesure est '%'*")


    st.markdown("##### <u> Jeux videos </u>",unsafe_allow_html=True)
    option_3 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de jeux videos préférées", ("Sexe", "Age"), key="selectbox_3")
    
    if option_3 == 'Age':
        game_age = pd.crosstab(df['tranche_age'], df['jeux_pref'], normalize='index')*100

        st.table(game_age)
        st.markdown("*NB: L'unite de mesure est '%'*")

    else : 
        game_sex = pd.crosstab(df['sexe'], df['jeux_pref'], normalize='index')*100
        
        st.table(game_sex)
        st.markdown("*NB: L'unite de mesure est '%'*")


    st.subheader("Taux dʼutilisation des différents appareils")
    appareils = df['appareils_utilises'].str.split(', ').explode()
    taux_utilisation_app = appareils.value_counts(normalize= True)*100

    st.table(taux_utilisation_app)
    st.markdown("*NB: L'unite de mesure est '%'*")

    


    st.subheader("Representation graphique (Chart)")
    st.markdown("##### Un histogramme du temps passé sur les réseaux sociaux")
    fig , ax = plt.subplots()
    ax.hist(df['temps_reseaux_sociaux_min'],color="#ff6f61", edgecolor="black")
    ax.set_facecolor("#f4f4f4")
    ax.set_title("Temps Passé sur les reseaux sociaux")
    ax.set_xlabel("Temps en minute", fontsize=12, color="#555")
    ax.set_ylabel("Nombre de personnes", fontsize=12, color="#555")
    # ax.legend()
    st.pyplot(fig)

    st.markdown("##### Un diagramme en barres des plateformes les plus utilisées")



    # Séparer les valeurs et compter les occurrences
    compteur_appareils = Counter()
    df['appareils_utilises'].dropna().apply(lambda x: compteur_appareils.update(x.split(', ')))

    # Convertir en DataFrame pour Matplotlib
    labels, values = zip(*compteur_appareils.items())

    fig2 , ax2 = plt.subplots()
    st.markdown("#####  Un camembert (Pie Chart) montrant la répartition des types d'appareils utilisés")
    ax2.pie(values, labels=labels)
    ax2.set_title("Répartition des types d'appareils utilisés")

    st.pyplot(fig2)


run()
