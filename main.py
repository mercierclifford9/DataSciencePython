import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import app as stl
import os

def run():

    """---------------------------------Netoyage des donnees---------------------------------"""
    # Recuperation du chemin vers le fichier de donnee 'data_digital_habits.csv'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(base_dir, "data", "data_digital_habits.csv")

    # Lecture du fchier 'data_digital_habits.csv'
    df = pd.read_csv(path_file)

    #Suppression des colonne avec les valeur null 'NaN'
    df.dropna(axis=1, how='all', inplace=True)

    #Suppression des colonnes comportant les valeurs '-- / 0'
    df=df.loc[ : , ~(df == '-- / 0').all(),]

    #Suppression des colonnes comportant les valeurs '0.00'
    df=df.loc[ : , ~(df == '0.00').all()]

    #Suppresion de la colonne score
    df.drop(inplace=True, columns=['Score total'])

    #Renommage des colonnes 
    df.columns=['date-heure','age','sexe', 'temps_streaming',
                'temps_jeux', 'reseau_social_pref', 'streaming_pref', 
                'jeux_pref','appareils_utilises','mode_consommation','Commentaires']
    df.drop(inplace=True, columns=['Commentaires'])
    
    #Formatage des colonnes
    df['date-heure'] = df['date-heure'].str.replace(" UTC−4", "")

    #Tirer que l'age dans le champs age
    df['age'] = df['age'].str.replace(r'[^\d]', '', regex=True)

    #Formatage du champs mode de consomation
    df['mode_consommation'] = (df['mode_consommation']
                                .str.replace("Avec des amis/ familles","Accompagne"))
    
    #Abreviation de Masculin et de Feminin
    df['sexe'] = df['sexe'].str.replace("Masculin","M")
    df['sexe'] = df['sexe'].str.replace("Féminin","F")

    #Dictionnaire de convertion de temps
    time_mapping = {
        'Moins de 30 minutes': 15,       # Valeur mediane
        'Entre 30 minutes et 1 heure': 45,
        'Entre 1 heure et 2 heures': 90,
        'Plus de 2 heures': 150           # 2h30 comme valeur representative
    }

    # Application du mappage du temps sur la serie 'temps_jeux'
    df['temps_jeux'] = (df['temps_jeux']
                            .map(time_mapping)
                            .fillna(0))  # Remplace les non-réponses par 0
    
    # Application du mappage du temps sur la serie 'temps_streaming'
    df['temps_streaming'] = (df['temps_streaming']
                            .map(time_mapping)
                            .fillna(0))  # Remplace les non-réponses par 0
    
    """typage des series"""
    #convertion generale des series en leur type 
    df=df.convert_dtypes()

    #convertion specifique de la serie 'date' en type datetime
    df['date-heure'] = (pd.to_datetime(df['date-heure'], 
                            format='%Y/%m/%d %I:%M:%S %p')) 
    
    #convertion specifique de la serie 'age' en int
    df['age'] = df['age'].astype('int64')

    #Calcul de la moyenne et de la mediane pour le temps passe dans les differentes actions
    analyse_desc = (df[['temps_streaming', 'temps_jeux']]
                    .agg(['mean', 'median'])
                    .rename(index={
                                    'mean' : 'Moyenne',
                                    'median' : 'Mediane'
                                    }
                            )
                    )
    
    # Création de la serie des tranches d'âge
    df['tranche_age'] = pd.cut(df['age'], 
                                bins=[0, 20, 25, 30, 100], 
                                labels=['<20', '20-25', '26-30', '30+'])
    

    """---------------------------------Analyse des donnees du dataframe---------------------------------"""
    
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
    taux_utilisation_app = df['appareils_utilises'].value_counts(normalize= True)*100


    print("\nAnalyse descriptive(moyenne et mediane)")
    print(analyse_desc.round(1))
    print("NB: Unite de mesure 'minute'\n")

    print("\nRepartion des plateformes de reseau social preferees par tranches d'age en %")
    print(social_age.round(1))
    print("NB: Unite de mesure '%'\n")
    print("\nRepartion des plateformes de reseau social preferees par sexe en %")
    print(social_sexe.round(1).rename(index={'M' : 'Masculin', 'F' : 'Feminin'}))
    print("NB: Unite de mesure '%'\n")

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

    df.to_csv("./data/Corrige.csv")
    # print(df.dtypes)

    # print(df)

    stl.write("hello")













if __name__ == "__main__":
    run()