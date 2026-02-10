# 🚨 Projet de Détection de Fraude sur Transactions Financières
## (Ingénierie de Données & Intelligence Artificielle)

---

## 📌 Présentation du projet

Ce projet vise à concevoir un **système de détection de transactions frauduleuses** à partir de données financières, en combinant **ingénierie de données, analyse exploratoire et modélisation en intelligence artificielle**.

Il s'inspire directement des problématiques rencontrées par les **fintechs, banques et opérateurs Mobile Money** (Wave, Orange Money, Free Money), particulièrement dans le **contexte africain et sénégalais**.

---

## 🎯 Objectifs

✅ Comprendre et analyser des données transactionnelles  
✅ Identifier des patterns de fraude  
✅ Préparer des données pour un modèle d'IA  
✅ Construire un modèle de détection de fraude interprétable  
✅ Simuler un cas réel de prévention des risques financiers  

---

## 🧠 Problématique métier

La **fraude financière** représente un risque majeur pour les plateformes de paiement. L'objectif est de répondre à des questions telles que :

- ❓ Quelles transactions présentent un risque élevé ?
- ❓ Existe-t-il des heures ou types de transactions plus frauduleux ?
- ❓ Comment automatiser la détection des comportements suspects ?
- ❓ Quels sont les patterns spécifiques au contexte sénégalais ?

---

## 🗂 Description du jeu de données

### 📄 Type de données

- **Données transactionnelles simulées**
- Inspirées de **cas réels Mobile Money et bancaires**
- Basées sur des **études de fraude en Afrique de l'Ouest** (GSMA, GIABA, BCEAO)

### 📦 Taille du dataset

- **100 000 transactions** sur 6 mois (juillet-décembre 2024)
- **~6 000 fraudes** détectées (taux réaliste de ~6%)
- **Taille** : ~50 MB

### 📑 Colonnes principales

| Colonne | Description |
|---------|-------------|
| `transaction_id` | Identifiant unique de la transaction |
| `date` | Date de la transaction |
| `hour` | Heure de la transaction (0-23) |
| `user_id` | Identifiant utilisateur (format téléphone sénégalais) |
| `amount` | Montant de la transaction (FCFA) |
| `transaction_type` | Type (transfer, payment, withdrawal, deposit) |
| `city` | Ville (Dakar, Thiès, Kaolack, Saint-Louis, Ziguinchor, Touba) |
| `operator` | Opérateur (Orange Money, Wave, Free Money, Wizall) |
| `nb_transactions_24h` | Nombre de transactions dans les dernières 24h |
| `changement_localisation` | Changement rapide de localisation (0/1) |
| `appareil_different` | Appareil différent utilisé (0/1) |
| `is_fraud` | **Indicateur de fraude** (0 = normal, 1 = suspect) |
| `fraud_type` | Type de fraude détecté |

### 🚨 Types de fraudes simulés

Basés sur des études réelles (GSMA, GIABA, BCEAO) :

1. **Phishing** (58-72% des fraudes) : Ingénierie sociale, faux agents
2. **SIM Swap** (15%) : Échange frauduleux de carte SIM
3. **Bypass Cash-In** (12%) : Fractionnement de dépôts par agents (35 951 cas OFMS 2019)
4. **Intrusion Compte Interne** (5%) : Usurpation d'habilitations
5. **Fermes SIM** (5%) : Multiples cartes SIM pour micro-transactions
6. **Agent Complice** (3%) : Vol de téléphone distributeur

### 📌 Remarque sur le déséquilibre

Le dataset est **volontairement déséquilibré** (~6% de fraudes), ce qui reflète les cas réels et constitue un **défi technique** pour la modélisation.

---

## 🛠 Technologies utilisées

- **Python 3.12**
- **Pandas** / **NumPy** - Manipulation de données
- **Scikit-learn** - Machine Learning
- **Matplotlib** / **Seaborn** - Visualisation
- **Imbalanced-learn** - Traitement du déséquilibre
- **XGBoost** - Modèle avancé (optionnel)
- **Jupyter Notebook** - Analyses interactives
- **Git & GitHub** - Versioning

---

## 🏗 Structure du projet

```
fraud-detection-project/
│
├── data/
│   └── transactions.csv              # Dataset (100K transactions)
│
├── notebooks/
│   ├── 01_exploration.ipynb          # Exploration des données
│   ├── 02_preprocessing.ipynb        # Prétraitement & Feature Engineering
│   └── 03_modeling.ipynb             # Modélisation IA
│
├── scripts/
│   └── generate_transactions.py      # Générateur de données
│
├── README.md                         # Documentation (ce fichier)
└── requirements.txt                  # Dépendances Python
```

---

## 🔄 Pipeline du projet

### 1️⃣ Exploration des données
- Analyse de la structure
- Identification des déséquilibres
- Compréhension des variables clés
- Visualisation des patterns de fraude

### 2️⃣ Prétraitement & Feature Engineering
- Nettoyage des données
- Encodage des variables catégorielles (One-Hot Encoding)
- Normalisation des montants
- Création de variables temporelles (jour de la semaine, période)
- Gestion du déséquilibre (SMOTE, Random Under-sampling)

### 3️⃣ Modélisation IA
- **Modèles utilisés** :
  - Régression Logistique (baseline)
  - Random Forest (modèle principal)
  - XGBoost (optionnel - performance maximale)
- **Évaluation avec** :
  - Precision
  - Recall
  - F1-score
  - AUC-ROC
  - Matrice de confusion
- **Interprétabilité** : Feature Importance

---

## 📈 Résultats clés attendus

- ✅ Identification de transactions à haut risque
- ✅ Mise en évidence des périodes et types de transactions sensibles
- ✅ Modèle capable de détecter la fraude avec **Recall > 80%**
- ✅ Approche explicable et adaptée à un usage métier
- ✅ Réduction des faux positifs (False Positive Rate < 5%)

---

## 🌍 Contexte sénégalais et africain

### Sources de données réelles utilisées

1. **GSMA** (2022-2024) : Statistiques Mobile Money en Afrique
2. **GIABA** (2019) : Typologies de fraude en Afrique de l'Ouest
3. **BCEAO** (2019) : 41 894 cas de fraude répertoriés (UEMOA)
4. **Orange Money Sénégal** : 35 951 cas de "Bypass Cash-In"
5. **Études académiques** : Taux de fraude de 3-6% (réaliste)

### Spécificités du contexte

- **43% des utilisateurs** ont fait face à une tentative de fraude (FinDev Gateway, 2023)
- **Phishing = 58-72%** des fraudes (GSMA)
- **SIM Swap** : Menace croissante en Afrique
- **Agents complices** : Problème récurrent
- **Faible bancarisation** : Mobile Money = cible privilégiée

### Opérateurs couverts

- **Orange Money** (40% des transactions) - Leader historique
- **Wave** (35%) - Challenger récent
- **Free Money** (15%)
- **Wizall** (10%)

---

## 🚀 Exécution du projet

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Génération des données (optionnel)

```bash
python scripts/generate_transactions.py
```

**Résultat attendu :**
```
✅ Dataset sauvegardé : data/transactions.csv
📊 Taille : 50.38 MB
🚨 Fraudes : 6,011 (6.01%)
```

### Exploration et modélisation

Ouvrir les notebooks dans l'ordre :
```bash
jupyter notebook notebooks/
```

1. `01_exploration.ipynb` - Comprendre les données
2. `02_preprocessing.ipynb` - Préparer les features
3. `03_modeling.ipynb` - Entraîner et évaluer les modèles

---

## 🎓 Compétences démontrées

### Compétences techniques

- 🐍 **Python** : Pandas, NumPy, Scikit-learn
- 🤖 **Machine Learning** : Classification, déséquilibre de classes
- 📊 **Analyse de données** : EDA, visualisation, statistiques
- 🧪 **Feature Engineering** : Création de variables pertinentes
- 🎯 **Évaluation de modèles** : Métriques, validation croisée

### Compétences méthodologiques

- 🔍 **Recherche documentaire** : Études GSMA, GIABA, BCEAO
- 🎯 **Contextualisation** : Adaptation au marché sénégalais
- 📝 **Documentation** : Code commenté, README détaillé
- 🧪 **Rigueur scientifique** : Méthodologie reproductible

---

## 💡 Intérêt du projet

✔️ Reflète un **cas d'usage réel** en fintech  
✔️ Démontre la **maîtrise du ML** sur données déséquilibrées  
✔️ Adapté au **contexte africain** (Mobile Money)  
✔️ **Interprétable** et orienté métier  
✔️ Pertinent pour **stages et emplois** en Data Science / IA  

---

## 🔮 Améliorations futures

- [ ] Intégration **en temps réel** (streaming avec Kafka)
- [ ] Modèles avancés (**XGBoost**, **LightGBM**, **Isolation Forest**)
- [ ] **Deep Learning** (LSTM pour séquences temporelles)
- [ ] **Déploiement via API** (FastAPI, Docker)
- [ ] Connexion à une base de données (**PostgreSQL**)
- [ ] **Système d'alerte automatique** (Slack, Email)
- [ ] **Dashboard interactif** (Streamlit, Dash)
- [ ] **Explainability** avancée (SHAP, LIME)

---

## 📊 Métriques d'évaluation

### Pourquoi pas seulement l'Accuracy ?

Avec **6% de fraudes**, un modèle qui prédit toujours "normal" aurait **94% d'accuracy** mais serait **inutile** !

### Métriques pertinentes

- **Recall (Sensibilité)** : % de fraudes correctement détectées → **Priorité #1**
- **Precision** : % de vraies fraudes parmi les alertes → Éviter les faux positifs
- **F1-Score** : Équilibre Precision-Recall
- **AUC-ROC** : Performance globale

### Objectifs cibles

| Métrique | Objectif |
|----------|----------|
| Recall | > 80% |
| Precision | > 60% |
| F1-Score | > 0.70 |
| AUC-ROC | > 0.90 |

---

## 👤 Auteur

**Oumaro Titans DJIGUIMDE**  
Étudiant en Ingénierie de Données et Intelligence Artificielle  
📍 Sénégal  

---

## 📚 Références

### Études et rapports

- [GSMA - State of the Industry Report on Mobile Money (2022-2024)](https://www.gsma.com/mobilefordevelopment/resources/)
- [GIABA - Typologies de Blanchiment liées à la Cybercriminalité](https://www.giaba.org/)
- [BCEAO - Direction des Systèmes et Moyens de Paiement](https://www.bceao.int/)
- [FinDev Gateway - Défis Mobile Money Sénégal (2023)](https://www.findevgateway.org/)

### Articles techniques

- [Synaptique - Types of Mobile Money Fraud (2025)](https://www.synaptique.com/)
- [Jeune Afrique - Comment le Mobile Money se protège (2023)](https://www.jeuneafrique.com/)
- [Financial Afrik - SIM Swap en Afrique (2025)](https://www.financialafrik.com/)

---

## 📣 Conclusion

Ce projet démontre une **approche professionnelle** de la détection de fraude, combinant **données, analyse et intelligence artificielle**, et constitue un excellent support pour des **candidatures en stage ou premier emploi** en Data Science et IA.

Le choix d'un **contexte sénégalais** reflète une volonté de valoriser les **réalités locales** et de montrer une capacité à **adapter les compétences techniques au terrain**.

---

⭐ **Si ce projet vous intéresse, n'hésitez pas à le cloner et l'adapter à vos besoins !**

**#DataScience #MachineLearning #FraudDetection #MobileMoney #Senegal #AI**
