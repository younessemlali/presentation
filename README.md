# 📊 Générateur de Présentations Automatiques - Rapports Téléphonie

Une application Streamlit qui transforme automatiquement vos rapports PDF de performance téléphonique en présentations interactives et rapports PowerPoint professionnels.

## ✨ Fonctionnalités Principales

- **📄 Parsing PDF Intelligent** : Extraction automatique des données structurées
- **📊 Visualisations Interactives** : Graphiques dynamiques avec Plotly
- **🎯 KPI Automatiques** : Calcul et affichage des indicateurs clés
- **👥 Analyse des Agents** : Performance individuelle et comparative
- **📈 Analyse de Tendances** : Évolution temporelle et prédictions
- **📋 Rapports PowerPoint** : Génération automatique de présentations
- **💾 Export Multi-format** : PowerPoint, Excel, PDF
- **🤖 Recommandations IA** : Suggestions d'amélioration automatiques

## 🚀 Installation et Déploiement

### Installation Locale

```bash
# Cloner le repository
git clone https://github.com/votre-username/rapport-pdf-generator.git
cd rapport-pdf-generator

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Déploiement sur Streamlit Cloud

1. Forkez ce repository sur votre GitHub
2. Connectez-vous sur [Streamlit Cloud](https://streamlit.io/cloud)
3. Cliquez sur "New app" et sélectionnez votre repository
4. L'app sera automatiquement déployée !

## 📁 Structure du Projet

```
rapport-pdf-generator/
├── app.py                     # Application principale Streamlit
├── requirements.txt           # Dépendances Python
├── README.md                 # Documentation
├── .gitignore               # Fichiers à ignorer
└── utils/
    ├── pdf_parser.py        # Parser PDF avancé
    ├── visualizations.py   # Générateur de graphiques
    └── report_generator.py # Export PowerPoint
```

## 🛠️ Technologies Utilisées

- **Frontend** : Streamlit
- **Visualisations** : Plotly, Matplotlib
- **Traitement PDF** : PyPDF2, pdfplumber
- **Données** : pandas, numpy
- **Export** : python-pptx, openpyxl
- **Déploiement** : Streamlit Cloud, GitHub

## 📖 Guide d'Utilisation

### 1. Upload du Rapport PDF

- Utilisez la sidebar pour uploader votre fichier PDF
- Formats supportés : Rapports de performance téléphonique
- Taille max : 50 MB

### 2. Configuration de l'Analyse

- **Parser avancé** : Extraction intelligente des données
- **Analyse des tendances** : Calculs prédictifs
- **Recommandations automatiques** : Suggestions IA

### 3. Exploration des Résultats

#### Dashboard Principal
- Vue d'ensemble des KPI
- Graphiques interactifs
- Alertes de performance

#### Analyse Mensuelle
- Évolution temporelle
- Données détaillées par mois
- Calcul des tendances

#### Performance des Agents
- Comparaison individuelle
- Classement et répartition
- Analyse de productivité

#### Rapport Exécutif
- Synthèse automatique
- Points forts et axes d'amélioration
- Recommandations personnalisées

### 4. Export des Résultats

- **PowerPoint** : Présentation complète prête à présenter
- **Excel** : Données brutes pour analyse approfondie
- **PDF** : Rapport statique (en développement)

## 🎯 Métriques Supportées

### KPI Principaux
- Volume total d'appels (présentés/traités)
- Taux de résolution global
- Durée moyenne de conversation
- Nombre d'agents actifs

### Analyses Avancées
- Tendances mensuelles
- Performance comparative des agents
- Indices de satisfaction (calculés)
- Ratios de productivité

### Alertes Automatiques
- Seuils de performance configurables
- Alertes visuelles en temps réel
- Suggestions d'actions correctives

## 📊 Exemples de Visualisations

L'application génère automatiquement :

1. **Graphiques en Barres** - Volume d'appels mensuel
2. **Courbes de Tendance** - Évolution des KPI
3. **Graphiques Radar** - Performance multi-critères
4. **Heatmaps** - Intensité d'activité
5. **Graphiques en Secteurs** - Répartition par agent
6. **Indicateurs Gauges** - Scores de performance

## ⚙️ Configuration Avancée

### Seuils d'Alerte
- Taux de résolution minimum : 85-98%
- Durée maximum conversation : 3-10 min
- Volume minimum mensuel : configurable

### Personnalisation
- Couleurs et thèmes
- Seuils de performance
- Formats d'export

## 🐛 Dépannage

### Problèmes Courants

**Erreur de parsing PDF**
- Vérifiez que le PDF contient du texte extractible
- Essayez avec l'option "Parser basique"

**Visualisations manquantes**
- Vérifiez que les données sont correctement extraites
- Consultez les logs dans la console

**Export PowerPoint échoue**
- Vérifiez que python-pptx est installé
- Redémarrez l'application

### Logs et Debugging

L'application affiche les erreurs dans l'interface. Pour plus de détails :

```bash
streamlit run app.py --logger.level=debug
```

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changes (`git commit -m 'Ajouter nouvelle fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

### Guidelines de Développement

- Code Python propre et documenté
- Tests unitaires pour nouvelles fonctionnalités
- Documentation mise à jour
- Respect des standards PEP 8

## 📝 Roadmap

### Version Actuelle (v1.0)
- ✅ Parsing PDF basique et avancé
- ✅ Visualisations interactives
- ✅ Export PowerPoint
- ✅ Interface utilisateur intuitive

### Prochaines Versions

#### v1.1
- [ ] Support de formats PDF additionnels
- [ ] Améliorations de l'IA de recommandations
- [ ] Templates PowerPoint personnalisables
- [ ] API REST pour intégration

#### v1.2
- [ ] Analyse prédictive avancée
- [ ] Alertes email automatiques
- [ ] Tableau de bord temps réel
- [ ] Support multi-langues

#### v2.0
- [ ] Machine Learning pour prédictions
- [ ] Intégration bases de données
- [ ] Authentification utilisateurs
- [ ] Version mobile

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙋‍♂️ Support

Pour toute question ou problème :

- 🐛 Issues GitHub : [Créer un ticket](https://github.com/votre-username/rapport-pdf-generator/issues)
- 📖 Documentation : [Wiki du projet](https://github.com/votre-username/rapport-pdf-generator/wiki)

## 🏆 Remerciements

- Équipe Streamlit pour l'excellent framework
- Communauté Plotly pour les visualisations
- Contributors et beta-testeurs

---

**Développé avec ❤️ pour automatiser vos rapports de performance**
