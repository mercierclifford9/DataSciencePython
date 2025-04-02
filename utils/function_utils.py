import pandas as pd




def data_cleaning(df:pd.DataFrame)->pd.DataFrame:
    # Lecture du fchier 'data_digital_habits.csv'

    #Suppression des colonne avec les valeur null 'NaN'
    df.dropna(axis=1, how='all', inplace=True)

    #Renommage des colonnes 
    df.columns=['date-heure','email','age','sexe', 'temps_reseaux_sociaux_min', 'temps_streaming_min',
                'temps_jeux_min', 'reseau_social_pref', 'streaming_pref', 
                'jeux_pref','appareils_utilises','mode_consommation']
        
    #Abreviation de Masculin et de Feminin
    df['sexe'] = df['sexe'].str.replace("Masculin","M")
    df['sexe'] = df['sexe'].str.replace("Féminin","F")

    #Dictionnaire de convertion de temps
    time_mapping = {
        'Moins de 30 minutes': 15,       # Valeur mediane
        'Entre 30 minutes et 1 heure': 45,
        'Entre 1 heure et 2 heures': 90,
        'Entre 2 heure et 3 heures': 150,
        'Entre 3 heure et 4 heures': 210,
        'Entre 4 heure et 5 heures': 270,
        'Plus de 5 heures': 330           # 5h30 comme valeur representative
    }

    # Application du mappage du temps sur la serie 'temps_jeux_min'
    df['temps_jeux_min'] = (df['temps_jeux_min']
                            .map(time_mapping)
                            .fillna(0))  # Remplace les non-réponses par 0
    
    # Application du mappage du temps sur la serie 'temps_streaming_min'
    df['temps_streaming_min'] = (df['temps_streaming_min']
                            .map(time_mapping)
                            .fillna(0))  # Remplace les non-réponses par 0
    
    # Application du mappage du temps sur la serie 'temps_reseaux_sociaux_min'
    df['temps_reseaux_sociaux_min'] = (df['temps_reseaux_sociaux_min']
                                        .map(time_mapping)
                                        .fillna(0))
    
    """typage des series"""
    #convertion generale des series en leur type 
    df=df.convert_dtypes()

    #convertion specifique de la serie 'date' en type datetime
    df['date-heure'] = (pd.to_datetime(df['date-heure'], 
                            format='%d/%m/%Y %H:%M:%S')) 
    
    #convertion specifique de la serie 'age' en int
    df['age'] = df['age'].astype('int64')

    # Création de la serie des tranches d'âge
    df['tranche_age'] = pd.cut(df['age'], 
                                bins=[0, 19, 25, 30, 100], 
                                labels=['<20', '20-25', '26-30', '30+'])
    
    return df


def mean_median (df:pd.DataFrame)->pd.DataFrame:

    analyse_desc = (df[['temps_streaming_min', 'temps_jeux_min', 'temps_reseaux_sociaux_min']]
                    .agg(['mean', 'median'])
                    .rename(index={
                                    'mean' : 'Moyenne',
                                    'median' : 'Mediane'
                                    }
                            )
                    )
    
    return analyse_desc

def update_data(df:pd.DataFrame, path_file:str):
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFgbbnrmGwc4ZsUr" \
            "LERjoTbRK6ltQiUoL732Xi5bsvoRfrXO4Oq-Q5bqlSbpWm0yUnHGaXaETXEhqR/pub?output=csv"
    
    # Lecture de l'Url
    df = pd.read_csv(url)

    #Enregistrement de la mise a jour du dataframe
    df.to_csv(path_file)
