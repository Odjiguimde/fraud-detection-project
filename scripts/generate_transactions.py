#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Génération de Transactions - Détection de Fraude
===========================================================

Génère un dataset de transactions Mobile Money avec patterns de fraude
basés sur le contexte sénégalais et ouest-africain.

Auteur: Oumaro Titans DJIGUIMDE
Date: Février 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
np.random.seed(42)
random.seed(42)

# ============================================================================
# TYPES DE FRAUDES BASÉS SUR LE CONTEXTE SÉNÉGALAIS
# ============================================================================

TYPES_FRAUDES = {
    'phishing': {
        'description': 'Ingénierie sociale (58-72% des fraudes)',
        'probabilite': 0.60,
        'montant_moyen': 35000,
        'heures_favorables': list(range(9, 18)),  # Heures de bureau
    },
    'sim_swap': {
        'description': 'Échange frauduleux de carte SIM',
        'probabilite': 0.15,
        'montant_moyen': 150000,
        'heures_favorables': list(range(22, 6)) + list(range(0, 6)),  # Nuit
    },
    'bypass_cash_in': {
        'description': 'Fractionnement de dépôts par agents (35,951 cas OFMS)',
        'probabilite': 0.12,
        'montant_moyen': 8000,
        'heures_favorables': list(range(8, 20)),
    },
    'compte_interne': {
        'description': 'Intrusion plateforme et usurpation habilitations',
        'probabilite': 0.05,
        'montant_moyen': 250000,
        'heures_favorables': list(range(0, 6)),  # Tard dans la nuit
    },
    'fermes_sim': {
        'description': 'Multiples cartes SIM pour micro-transactions',
        'probabilite': 0.05,
        'montant_moyen': 5000,
        'heures_favorables': list(range(0, 24)),  # 24/7
    },
    'agent_complice': {
        'description': 'Agent complice (vol téléphone distributeur)',
        'probabilite': 0.03,
        'montant_moyen': 45000,
        'heures_favorables': list(range(18, 23)),
    }
}

# Villes sénégalaises
VILLES = {
    'Dakar': 0.50,
    'Thiès': 0.15,
    'Kaolack': 0.12,
    'Saint-Louis': 0.10,
    'Ziguinchor': 0.08,
    'Touba': 0.05
}

# Types de transactions Mobile Money
TRANSACTION_TYPES = {
    'transfer': 0.45,      # Transfert P2P
    'payment': 0.25,       # Paiement marchand
    'withdrawal': 0.20,    # Retrait
    'deposit': 0.10        # Dépôt
}

# Opérateurs Mobile Money sénégalais
OPERATEURS = {
    'Orange Money': 0.40,
    'Wave': 0.35,
    'Free Money': 0.15,
    'Wizall': 0.10
}

# ============================================================================
# FONCTIONS DE GÉNÉRATION
# ============================================================================

def generer_montant_normal(transaction_type):
    """
    Génère un montant normal selon le type de transaction
    """
    ranges = {
        'transfer': (1000, 50000),
        'payment': (500, 30000),
        'withdrawal': (5000, 100000),
        'deposit': (5000, 200000)
    }
    
    min_val, max_val = ranges[transaction_type]
    
    # Distribution log-normale (plus réaliste)
    montant = np.random.lognormal(
        mean=np.log(min_val + (max_val - min_val) / 2),
        sigma=0.8
    )
    
    return max(min_val, min(max_val, montant))

def generer_montant_frauduleux(type_fraude):
    """
    Génère un montant frauduleux selon le type de fraude
    """
    config = TYPES_FRAUDES[type_fraude]
    base = config['montant_moyen']
    
    # Variation autour de la moyenne
    montant = base * np.random.uniform(0.5, 2.5)
    
    return montant

def est_heure_suspect(heure, type_fraude=None):
    """
    Détermine si l'heure est suspecte
    """
    # Heures suspectes générales: tard la nuit
    heures_suspectes = list(range(23, 24)) + list(range(0, 5))
    
    if type_fraude and type_fraude in TYPES_FRAUDES:
        heures_favorables = TYPES_FRAUDES[type_fraude]['heures_favorables']
        return heure in heures_favorables
    
    return heure in heures_suspectes

def generer_user_id():
    """
    Génère un user_id réaliste (format téléphone sénégalais)
    """
    # Format: +221 XX XXX XX XX
    prefixes = ['77', '78', '76', '70', '75']  # Préfixes sénégalais
    prefix = random.choice(prefixes)
    numero = f"{prefix}{random.randint(1000000, 9999999)}"
    return f"user_{numero}"

def determiner_si_fraude(transaction_type, heure, montant, date):
    """
    Détermine si une transaction doit être frauduleuse (dataset déséquilibré)
    """
    # Taux de fraude global: ~3-5% (réaliste selon études)
    taux_base = 0.04
    
    # Augmentation selon facteurs de risque
    facteur_risque = 1.0
    
    # Heure suspecte
    if est_heure_suspect(heure):
        facteur_risque *= 2.5
    
    # Montant élevé
    if montant > 100000:
        facteur_risque *= 2.0
    
    # Week-end (moins de surveillance)
    if date.weekday() >= 5:
        facteur_risque *= 1.5
    
    # Retrait (plus risqué)
    if transaction_type == 'withdrawal':
        facteur_risque *= 1.8
    
    probabilite_fraude = min(taux_base * facteur_risque, 0.15)  # Max 15%
    
    return np.random.random() < probabilite_fraude

def choisir_type_fraude():
    """
    Choisit un type de fraude selon les probabilités
    """
    types = list(TYPES_FRAUDES.keys())
    probas = [TYPES_FRAUDES[t]['probabilite'] for t in types]
    
    # Normaliser
    total = sum(probas)
    probas = [p / total for p in probas]
    
    return np.random.choice(types, p=probas)

def generer_features_suspectes(est_fraude, type_fraude=None):
    """
    Génère des features supplémentaires pour faciliter la détection
    """
    if est_fraude and type_fraude:
        # Transactions multiples du même user dans un court laps de temps
        nb_trans_recentes = np.random.randint(5, 20) if type_fraude == 'fermes_sim' else np.random.randint(1, 3)
        
        # Changement de localisation rapide
        changement_localisation = np.random.choice([True, False], p=[0.7, 0.3])
        
        # Appareil différent
        appareil_different = np.random.choice([True, False], p=[0.6, 0.4])
        
    else:
        nb_trans_recentes = np.random.randint(0, 3)
        changement_localisation = False
        appareil_different = False
    
    return {
        'nb_transactions_24h': nb_trans_recentes,
        'changement_localisation': changement_localisation,
        'appareil_different': appareil_different
    }

# ============================================================================
# GÉNÉRATION DU DATASET
# ============================================================================

def generer_transactions(n_transactions=100000):
    """
    Génère le dataset complet
    """
    print("="*70)
    print("🚨 GÉNÉRATION DE TRANSACTIONS - DÉTECTION DE FRAUDE 🚨")
    print("="*70)
    print(f"\n🔄 Génération de {n_transactions:,} transactions...")
    
    # Période: 6 mois
    date_debut = datetime(2024, 7, 1)
    date_fin = datetime(2024, 12, 31)
    jours_total = (date_fin - date_debut).days
    
    transactions = []
    users_pool = [generer_user_id() for _ in range(50000)]  # Pool de 50k users
    
    for i in range(n_transactions):
        if (i + 1) % 10000 == 0:
            print(f"   ✓ {i+1:,} / {n_transactions:,} transactions générées")
        
        # Date
        jour = np.random.randint(0, jours_total)
        date = date_debut + timedelta(days=jour)
        
        # Heure (distribution réaliste)
        # Plus d'activité en journée
        heures_probas = [0.01]*6 + [0.03]*2 + [0.08]*10 + [0.04]*4 + [0.02]*2
        heure = np.random.choice(range(24), p=np.array(heures_probas)/sum(heures_probas))
        
        # Type de transaction
        transaction_type = np.random.choice(
            list(TRANSACTION_TYPES.keys()),
            p=list(TRANSACTION_TYPES.values())
        )
        
        # Montant initial (normal)
        montant = generer_montant_normal(transaction_type)
        
        # Déterminer si fraude
        est_fraude = determiner_si_fraude(transaction_type, heure, montant, date)
        
        type_fraude = None
        if est_fraude:
            # Choisir type de fraude
            type_fraude = choisir_type_fraude()
            # Ajuster montant selon type de fraude
            montant = generer_montant_frauduleux(type_fraude)
        
        # Ville
        ville = np.random.choice(list(VILLES.keys()), p=list(VILLES.values()))
        
        # Opérateur
        operateur = np.random.choice(list(OPERATEURS.keys()), p=list(OPERATEURS.values()))
        
        # User ID
        if est_fraude and type_fraude == 'fermes_sim':
            # Fraudeur utilise multiples comptes
            user_id = generer_user_id()
        else:
            user_id = random.choice(users_pool)
        
        # Features suspectes
        features = generer_features_suspectes(est_fraude, type_fraude)
        
        # Construire la transaction
        transaction = {
            'transaction_id': f"TXN{i+1:08d}",
            'date': date.strftime('%Y-%m-%d'),
            'hour': heure,
            'user_id': user_id,
            'amount': round(montant, 0),
            'transaction_type': transaction_type,
            'city': ville,
            'operator': operateur,
            'nb_transactions_24h': features['nb_transactions_24h'],
            'changement_localisation': int(features['changement_localisation']),
            'appareil_different': int(features['appareil_different']),
            'is_fraud': int(est_fraude),
            'fraud_type': type_fraude if est_fraude else 'normal'
        }
        
        transactions.append(transaction)
    
    print(f"\n✅ Génération terminée : {len(transactions):,} transactions")
    
    # Créer DataFrame
    df = pd.DataFrame(transactions)
    
    return df

def afficher_statistiques(df):
    """
    Affiche les statistiques du dataset
    """
    print("\n" + "="*70)
    print("📊 STATISTIQUES DU DATASET")
    print("="*70)
    
    print(f"\n📌 Taille : {len(df):,} transactions")
    print(f"📅 Période : {df['date'].min()} → {df['date'].max()}")
    
    # Fraudes
    nb_fraudes = df['is_fraud'].sum()
    taux_fraude = (nb_fraudes / len(df)) * 100
    
    print(f"\n🚨 Fraudes :")
    print(f"   • Nombre : {nb_fraudes:,}")
    print(f"   • Taux : {taux_fraude:.2f}%")
    print(f"   • Normales : {len(df) - nb_fraudes:,} ({100-taux_fraude:.2f}%)")
    
    # Distribution par type de fraude
    print(f"\n📊 Types de fraudes :")
    fraudes_df = df[df['is_fraud'] == 1]
    if len(fraudes_df) > 0:
        types_counts = fraudes_df['fraud_type'].value_counts()
        for fraud_type, count in types_counts.items():
            pct = (count / len(fraudes_df)) * 100
            print(f"   • {fraud_type:20s} : {count:5d} ({pct:5.1f}%)")
    
    # Montants
    print(f"\n💰 Montants :")
    print(f"   • Normal moyen : {df[df['is_fraud']==0]['amount'].mean():,.0f} FCFA")
    print(f"   • Fraude moyen : {df[df['is_fraud']==1]['amount'].mean():,.0f} FCFA")
    print(f"   • Médiane : {df['amount'].median():,.0f} FCFA")
    
    # Répartition
    print(f"\n🏙️  Par ville :")
    print(df['city'].value_counts().head())
    
    print(f"\n📱 Par opérateur :")
    print(df['operator'].value_counts())
    
    print(f"\n💳 Par type de transaction :")
    print(df['transaction_type'].value_counts())
    
    print("\n" + "="*70)

# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    # Génération
    df = generer_transactions(n_transactions=100000)
    
    # Statistiques
    afficher_statistiques(df)
    
    # Sauvegarde
    output_path = 'data/transactions.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n✅ Dataset sauvegardé : {output_path}")
    print(f"📊 Taille : {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    print("\n" + "="*70 + "\n")
