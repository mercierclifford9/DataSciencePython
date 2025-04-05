import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils.function_utils import data_cleaning, mean_median, update_data


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

    col_1_1, col_1_2 = st.columns(2)
    with col_1_1 :
    #creation du bouton pour mettre a jour les donnees
        if st.button("Cliquer pour mettre a jour les donnees"):
            update_data(df, path_file)

    with col_1_2 :
        st.markdown("[Cliquer pour remplir le formulaire google form](https://docs.google.com/forms/d/e/1FAIpQLSfkp1Hu3z34fIyREIUKsO7FhhCWCNGP-aDLrLCeCqp94PWaxg/viewform?usp=header)")


    st.text(f"Pour commencer nous allons vous presentez les donnees brut avant nettoyage - {df.iloc[:, 0].count()} lignes de donnees")
    st.dataframe(df)


    df = data_cleaning(df) #Appel de notre foncion data_cleaning() declare dans function_utils.py
    st.text(f"Et voila les donnees apres nettoyage - {df.iloc[:, 0].count()} lignes de donnees")
    st.dataframe(df)
    # df.to_csv("./data/data_digital_hatits_clean.csv")


    st.subheader("Analyse descriptive")

    st.markdown("##### <u>Moyennes et médianes du temps passé par activité</u>", unsafe_allow_html=True)

    #Calcul de la moyenne et de la mediane pour le temps passe dans les differentes actions
    calc_mean_median = mean_median(df).round(2) #Appel de notre foncion mean_median() declare dans function_utilis.py
    st.dataframe(calc_mean_median) 
    st.write("*NB: Unite de mesure (minutes)*")

    st.subheader("Répartition des plateformes préférées par tranche dʼâge ou sexe")
    
    st.markdown("##### <u> Streaming </u>",unsafe_allow_html=True)
    option_1 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de streaming préférées", ("Sexe", "Age"), key="selectbox_1")

    if option_1 == 'Sexe':
        streaming_sexe = pd.crosstab(df['sexe'], df['streaming_pref'], normalize='index')*100
        streaming_sexe = streaming_sexe.round(2)

        st.dataframe(streaming_sexe.rename(index={'F':'Feminin', 'M':'Masculin'}))
        st.markdown("*NB: Unite de mesure (%)*")
    else : 
        streaming_age = pd.crosstab(df['tranche_age'], df['streaming_pref'], normalize='index')*100
        streaming_age = streaming_age.round(2)

        st.dataframe(streaming_age)
        st.markdown("*NB: Unite de mesure (%)*")

    st.markdown("##### <u> Reseaux Sociaux </u>",unsafe_allow_html=True)
    option_2 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de reseaux sociaux preferees", ("Sexe", "Age"), key="selectbox_2")
    
    if option_2 == 'Age':
        social_age = pd.crosstab(df['tranche_age'], df['reseau_social_pref'], normalize='index')*100
        social_age = social_age.round(2)

        st.dataframe(social_age)
        st.markdown("*NB: Unite de mesure (%)*")
    else : 
        social_sexe = pd.crosstab(df['sexe'], df['reseau_social_pref'], normalize='index')*100
        social_sexe = social_sexe.round(2)

        st.dataframe(social_sexe)
        st.markdown("*NB: Unite de mesure (%)*")


    st.markdown("##### <u> Jeux videos </u>",unsafe_allow_html=True)
    option_3 = st.selectbox("Veuillez choisir comment vous souhaitez avoir la repartition des "
                            "plateformes de jeux videos préférées", ("Sexe", "Age"), key="selectbox_3")
    
    if option_3 == 'Age':
        game_age = pd.crosstab(df['tranche_age'], df['jeux_pref'], normalize='index')*100
        game_age = game_age.round(2)

        st.dataframe(game_age)
        st.markdown("*NB: Unite de mesure (%)*")

    else : 
        game_sex = pd.crosstab(df['sexe'], df['jeux_pref'], normalize='index')*100
        game_sex = game_sex.round(2)

        st.dataframe(game_sex)
        st.markdown("*NB: Unite de mesure (%)*")


    st.subheader("Taux d'utilisation des differents appareils")
    appareils = df['appareils_utilises'].str.split(', ').explode()
    taux_utilisation_app = appareils.value_counts(normalize= True)*100
    taux_utilisation_app = taux_utilisation_app.round(2)
    st.dataframe(taux_utilisation_app)
    st.markdown("*NB: Unite de mesure (%)*")

# Bonus-------------------------------------
    st.subheader("Top 3 des plateformes les plus populaires")
    option_top3 = st.selectbox("Choisissez le critere de regroupement", ("Sexe", "Tranche d'age"))
    
    if option_top3 == "Sexe":
        top3_sex = df.groupby('sexe')['reseau_social_pref'].value_counts().groupby(level=0).head(3)
        st.dataframe(top3_sex)
    else:
        top3_age = df.groupby('tranche_age')['reseau_social_pref'].value_counts().groupby(level=0).head(3)
        st.dataframe(top3_age)


    


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

    bouton3 = st.selectbox("Choisissez la maniere dont vous souhaitez voir les donnees",('Trois Diagrammes distinct', 'Un seul Diagramme'), key = 'selectbox_10')

    if bouton3 =="Trois Diagrammes distinct":

        col_1, col_2, col_3 = st.columns(3)

        with col_1:
            st.text("Reseaux Sociaux")
            counts_1 = df['reseau_social_pref'].value_counts()
            fig_3_1, ax_3 = plt.subplots()
            ax_3.bar(counts_1.index, counts_1.values, color='#ff6f61' , edgecolor='black')
            ax_3.set_facecolor("#f4f4f4")
            ax_3.set_title("Temps Passé sur les reseaux sociaux")
            ax_3.set_xlabel("Plateforme", fontsize=12, color="#555")
            ax_3.set_ylabel("Nombre de personnes", fontsize=12, color="#555")
            st.pyplot(fig_3_1)

        with col_2:
            st.text("Streaming")
            counts_2 = df['streaming_pref'].value_counts()
            fig_3_2, ax_3 = plt.subplots()
            ax_3.bar(counts_2.index, counts_2.values, color='#ff6f61' , edgecolor='black')
            ax_3.set_facecolor("#f4f4f4")
            ax_3.set_title("Temps Passé sur les reseaux sociaux")
            ax_3.set_xlabel("Plateforme", fontsize=12, color="#555")
            ax_3.set_ylabel("Nombre de personnes", fontsize=12, color="#555")
            st.pyplot(fig_3_2)


        with col_3:
            st.text("Jeux video")
            counts_3 = df['jeux_pref'].value_counts()
            fig_3_3, ax_3 = plt.subplots()
            ax_3.bar(counts_3.index, counts_3.values, color='#ff6f61' , edgecolor='black') 
            ax_3.set_facecolor("#f4f4f4")
            ax_3.set_title("Temps Passé sur les reseaux sociaux")
            ax_3.set_xlabel("Plateforme", fontsize=12, color="#555")
            ax_3.set_ylabel("Nombre de personnes", fontsize=12, color="#555")
            st.pyplot(fig_3_3)

        st.text("Cliquez sur l'icone ⛶ dans le graphique pour le voir en plein ecran")
    else:
        fig_3 , ax_3 =plt.subplots()
        plateform = pd.concat([
            df["reseau_social_pref"].str.split(', ').explode(),
            df["streaming_pref"].str.split(', ').explode(),
            df["jeux_pref"].str.split(', ').explode()
        ]).value_counts()
        ax_3.bar(plateform.index.map(str), plateform.values, color='#ff6f61' , edgecolor='black')
        plt.xticks(rotation=60)  # Remplacez 45 par 60 si vous voulez plus incliné

        st.pyplot(fig_3)



    # Separer les valeurs et compter les occurrences
    appareils = df['appareils_utilises'].dropna().str.split(', ').explode()

    compteur_appareils = appareils.value_counts(normalize=True) * 100
    



    labels, values = zip(*compteur_appareils.items())
    colors = ['#FF6F61','#6B5B95', '#88B04B', '#F7B7A3', '#FFCC00']

    fig2, ax2 = plt.subplots()
    st.markdown("#####  Un camembert (Pie Chart) montrant la répartition des types d'appareils utilisés")

    # Camembert sans labels
    wedges, texts, autotexts = ax2.pie(
        values, autopct="%1.1f%%", colors=colors, startangle=90
    )

    # Ajout legende alignee a droite
    ax2.legend(wedges,labels, title="Appareils",
        loc="center left",
        bbox_to_anchor=(1, 0.5),  # Position a droite
        frameon=False
    )

    ax2.set_title("Repartition des types d'appareils utilises")

    # Affichage dans Streamlit
    st.pyplot(fig2)


    st.markdown("##### Graphique en ligne : Evolution du temps passe par age")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='tranche_age', y='temps_reseaux_sociaux_min', marker="o", ax=ax)
    ax.set_title("Évolution du temps passe sur les réseaux sociaux par age")
    ax.set_xlabel("Tranche d'age")
    ax.set_ylabel("Temps (minutes)")
    st.pyplot(fig)


    # conclusion des tendances observees.

    st.markdown("#### Résumé de l'analyse des habitudes de consommation numérique")

    st.markdown("##### Statistiques clés")

    st.markdown("""
    - **Profil démographique :**  
    58% d'hommes, 42% de femmes  
    75% ont entre 20 et 25 ans

    - **Usage quotidien moyen :**  
    **Réseaux sociaux :** 3h16 min  
    **Streaming vidéo :** 2h16 min  
    **Jeux vidéo :** 1h02 min  

    - **Plateformes les plus utilisées :**  
    **Réseaux sociaux :** WhatsApp, Instagram, TikTok  
    **Streaming :** Netflix, YouTube  
    **Jeux :** PlayStation en tête

    - **Appareils dominants :**  
    98% utilisent un **smartphone**, suivis des laptops et tablettes

    - **Mode de consommation :**  
    87% consomment seuls
    """)

    # conclusion encadre
    st.info("""
    Ces résultats montrent une forte **dépendance aux contenus numériques mobiles**, surtout chez les **jeunes adultes connectés** via des plateformes sociales et de streaming.  
    Cela offre des **opportunités stratégiques** pour le marketing digital, le divertissement mobile et les services personnalisés.
    """)



run()
