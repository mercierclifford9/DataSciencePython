import pandas as pd
from matplotlib import pyplot as plt
from utils.function_utils import data_cleaning, mean_median, update_data

import os

def run():

    """Netoyage des donnees(Data cleaning)"""
    # Recuperation du chemin vers le fichier de donnee 'data_digital_habits.csv'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(base_dir, "data", "data_digital_habits.csv")

    # Lecture du fchier 'data_digital_habits.csv'
    df = pd.read_csv(path_file, index_col=0)

    df = data_cleaning(df) #Appel de notre foncion data_cleaning() declare dans function_utils.py
    """Analyse des donnees du dataframe(Data Analysis)"""
    analyse_desc = mean_median(df)
    """Plateforme de streaming"""
    #repartion des plateformes de streaming preferees par tranches d'age
    streaming_age = pd.crosstab(df['tranche_age'], df['streaming_pref'], normalize='index')*100

    #Repartion des plateformes de streaming preferees par sexe
    streaming_sexe = pd.crosstab(df['sexe'], df['streaming_pref'], normalize='index')*100

    """Platerforme de reseaux sociaux"""
    #repartion des plateformes de streaming preferees par tranches d'age
    social_age = pd.crosstab(df['tranche_age'], df['reseau_social_pref'], normalize='index')*100

    #Repartion des plateformes de streaming preferees par sexe
    social_sexe = pd.crosstab(df['sexe'], df['reseau_social_pref'], normalize='index')*100

    """Plateforme de jeux video"""
    #repartion des plateformes de streaming preferees par tranches d'age
    game_age = pd.crosstab(df['tranche_age'], df['jeux_pref'], normalize='index')*100

    #Repartion des plateformes de streaming preferees par sexe
    game_sex = pd.crosstab(df['sexe'], df['jeux_pref'], normalize='index')*100


    """Taux d'utilisation des differents appareils"""
    appareil = df['appareils_utilises'].str.split(', ').explode()
    taux_utilisation_app = appareil.value_counts(normalize= True)*100


    print("\nAnalyse descriptive(moyenne et mediane)")
    print(analyse_desc.round(1))
    print("NB: Unite de mesure 'minute'\n")

    print("\nRepartion des plateformes de reseau social preferees par tranches d'age en %")
    print(social_age.round(1))
    print("NB: Unite de mesure '%'\n")
    print("\nRepartion des plateformes de reseau social preferees par sexe en %")
    print(social_sexe.round(1).rename(index={'M' : 'Masculin', 'F' : 'Feminin'}))
    print("NB: L'unite de mesure est '%'\n")

    print("\nRepartion des plateformes de jeux preferees par tranches d'age en %")
    print(game_age.round(1))
    print("NB: Unite de mesure '%'\n")
    print("\nRepartion des plateformes de jeux preferees par sexe en %")
    print(game_sex.round(1))
    print("NB: Unite de mesure '%'\n")

    print("\nRepartion des plateformes de streaming preferees par tranches d'age en %")
    print(streaming_age.round(1))
    print("NB: Unite de mesure '%'\n")
    print("\nRepartion des plateformes de streaming preferees par sexe en %")
    print(streaming_sexe.round(1))
    print("NB: Unite de mesure '%'\n")

    print("Taux d'utilisation des differents appareils en %")
    print(taux_utilisation_app)
    print("NB: Unite de mesure '%'\n")

    df.to_csv("./data/corrected_data.csv")
    # print(df.dtypes)

    # print(df)

    df['temps_streaming_min'].hist(bins=5)
    plt.show()












if __name__ == "__main__":
    run()