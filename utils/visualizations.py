import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class TelephoneReportVisualizer:
    """Créateur de visualisations pour les rapports de téléphonie"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'accent': '#e74c3c',
            'warning': '#f39c12',
            'info': '#9b59b6',
            'success': '#27ae60',
            'dark': '#34495e'
        }
        
        self.template = "plotly_white"
    
    def create_monthly_performance_dashboard(self, monthly_data: pd.DataFrame) -> Dict[str, go.Figure]:
        """Crée un dashboard complet des performances mensuelles"""
        figures = {}
        
        if monthly_data.empty:
            return self._create_empty_figures()
        
        # 1. Graphique en barres groupées - Volume d'appels
        figures['volume_calls'] = self._create_volume_calls_chart(monthly_data)
        
        # 2. Graphique en aires empilées - Évolution temporelle
        figures['temporal_evolution'] = self._create_temporal_evolution_chart(monthly_data)
        
        # 3. Graphique en radar - Performance globale
        figures['performance_radar'] = self._create_performance_radar(monthly_data)
        
        # 4. Heatmap - Intensité d'activité
        figures['activity_heatmap'] = self._create_activity_heatmap(monthly_data)
        
        # 5. Indicateurs de tendance
        figures['trend_indicators'] = self._create_trend_indicators(monthly_data)
        
        return figures
    
    def _create_volume_calls_chart(self, df: pd.DataFrame) -> go.Figure:
        """Volume d'appels présentés vs traités"""
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=["Volume d'Appels Mensuels"]
        )
        
        # Barres pour appels présentés
        fig.add_trace(
            go.Bar(
                x=df['mois'],
                y=df.get('appels_presentes', []),
                name='Appels Présentés',
                marker_color=self.color_palette['primary'],
                opacity=0.8
            )
        )
        
        # Barres pour appels traités
        fig.add_trace(
            go.Bar(
                x=df['mois'],
                y=df.get('appels_traites', []),
                name='Appels Traités',
                marker_color=self.color_palette['secondary'],
                opacity=0.8
            )
        )
        
        # Ligne du taux de résolution
        if 'appels_presentes' in df and 'appels_traites' in df:
            taux_resolution = (df['appels_traites'] / df['appels_presentes'] * 100).fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=df['mois'],
                    y=taux_resolution,
                    name='Taux de Résolution (%)',
                    line=dict(color=self.color_palette['accent'], width=3),
                    marker=dict(size=8),
                    yaxis='y2'
                )
            )
        
        fig.update_layout(
            title="Volume d'Appels et Taux de Résolution",
            template=self.template,
            barmode='group',
            hovermode='x unified'
        )
        
        fig.update_yaxes(title_text="Nombre d'Appels", secondary_y=False)
        fig.update_yaxes(title_text="Taux de Résolution (%)", secondary_y=True, range=[80, 100])
        
        return fig
    
    def _create_temporal_evolution_chart(self, df: pd.DataFrame) -> go.Figure:
        """Évolution temporelle des métriques clés"""
        fig = go.Figure()
        
        # Durée moyenne de conversation
        if 'duree_moyenne_conv' in df:
            fig.add_trace(go.Scatter(
                x=df['mois'],
                y=df['duree_moyenne_conv'],
                mode='lines+markers',
                name='Durée Moyenne (min)',
                line=dict(color=self.color_palette['info'], width=3),
                marker=dict(size=10),
                fill='tonexty'
            ))
        
        # Nombre d'agents
        if 'nb_agents_max' in df:
            fig.add_trace(go.Scatter(
                x=df['mois'],
                y=df['nb_agents_max'],
                mode='lines+markers',
                name="Nombre d'Agents Max",
                line=dict(color=self.color_palette['warning'], width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))
        
        fig.update_layout(
            title="Évolution Temporelle des Métriques",
            template=self.template,
            hovermode='x unified',
            yaxis=dict(title="Durée (minutes)"),
            yaxis2=dict(title="Nombre d'Agents", overlaying='y', side='right')
        )
        
        return fig
    
    def _create_performance_radar(self, df: pd.DataFrame) -> go.Figure:
        """Graphique radar des performances moyennes"""
        # Calcul des moyennes
        metrics = []
        values = []
        
        if 'appels_traites' in df and not df['appels_traites'].empty:
            metrics.append('Volume Traité')
            values.append(df['appels_traites'].mean() / df['appels_traites'].max() * 100)
        
        if 'duree_moyenne_conv' in df and not df['duree_moyenne_conv'].empty:
            metrics.append('Efficacité Temps')
            # Inverser pour que moins de temps = meilleure performance
            values.append((df['duree_moyenne_conv'].max() - df['duree_moyenne_conv'].mean()) / df['duree_moyenne_conv'].max() * 100)
        
        if 'nb_agents_max' in df and not df['nb_agents_max'].empty:
            metrics.append('Utilisation Ressources')
            values.append(df['nb_agents_max'].mean() / df['nb_agents_max'].max() * 100)
        
        # Ajouter le taux de résolution si disponible
        if 'appels_presentes' in df and 'appels_traites' in df:
            metrics.append('Taux Résolution')
            taux_global = (df['appels_traites'].sum() / df['appels_presentes'].sum()) * 100
            values.append(taux_global)
        
        if not metrics:
            return go.Figure()
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],  # Fermer le polygone
            theta=metrics + [metrics[0]],
            fill='toself',
            name='Performance Globale',
            line_color=self.color_palette['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Radar des Performances",
            template=self.template
        )
        
        return fig
    
    def _create_activity_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Heatmap d'intensité d'activité"""
        if df.empty or 'mois' not in df:
            return go.Figure()
        
        # Créer une matrice pour la heatmap
        metrics = ['Appels Présentés', 'Appels Traités', 'Durée Moy.', 'Nb Agents']
        months = df['mois'].tolist()
        
        # Normaliser les données pour la heatmap
        data_matrix = []
        
        for metric in metrics:
            row = []
            if metric == 'Appels Présentés' and 'appels_presentes' in df:
                values = df['appels_presentes']
                normalized = (values - values.min()) / (values.max() - values.min()) * 100
                row = normalized.tolist()
            elif metric == 'Appels Traités' and 'appels_traites' in df:
                values = df['appels_traites']
                normalized = (values - values.min()) / (values.max() - values.min()) * 100
                row = normalized.tolist()
            elif metric == 'Durée Moy.' and 'duree_moyenne_conv' in df:
                values = df['duree_moyenne_conv']
                # Inverser pour que moins de temps = plus d'intensité
                normalized = (values.max() - values) / (values.max() - values.min()) * 100
                row = normalized.tolist()
            elif metric == 'Nb Agents' and 'nb_agents_max' in df:
                values = df['nb_agents_max']
                normalized = (values - values.min()) / (values.max() - values.min()) * 100 if values.max() > values.min() else [50] * len(values)
                row = normalized.tolist()
            
            if not row:
                row = [0] * len(months)
            data_matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=data_matrix,
            x=months,
            y=metrics,
            colorscale='RdYlBu_r',
            showscale=True,
            colorbar=dict(title="Intensité")
        ))
        
        fig.update_layout(
            title="Heatmap d'Intensité d'Activité",
            template=self.template
        )
        
        return fig
    
    def _create_trend_indicators(self, df: pd.DataFrame) -> go.Figure:
        """Indicateurs de tendance avec flèches"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Tendance Volume', 'Tendance Qualité', 'Tendance Efficacité', 'Tendance Ressources'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Calculs des tendances
        trends = self._calculate_trends(df)
        
        # Volume
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=trends.get('volume_trend', 0),
            delta={'reference': 0},
            gauge={'axis': {'range': [-100, 100]},
                   'bar': {'color': self.color_palette['primary']}},
            title={'text': "Volume"},
        ), row=1, col=1)
        
        # Qualité (taux de résolution)
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=trends.get('quality_trend', 0),
            delta={'reference': 0},
            gauge={'axis': {'range': [-100, 100]},
                   'bar': {'color': self.color_palette['secondary']}},
            title={'text': "Qualité"},
        ), row=1, col=2)
        
        # Efficacité (durée)
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=trends.get('efficiency_trend', 0),
            delta={'reference': 0},
            gauge={'axis': {'range': [-100, 100]},
                   'bar': {'color': self.color_palette['info']}},
            title={'text': "Efficacité"},
        ), row=2, col=1)
        
        # Ressources
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=trends.get('resources_trend', 0),
            delta={'reference': 0},
            gauge={'axis': {'range': [-100, 100]},
                   'bar': {'color': self.color_palette['warning']}},
            title={'text': "Ressources"},
        ), row=2, col=2)
        
        fig.update_layout(title="Indicateurs de Tendance", template=self.template)
        
        return fig
    
    def create_agents_performance_dashboard(self, agents_data: pd.DataFrame) -> Dict[str, go.Figure]:
        """Dashboard de performance des agents"""
        figures = {}
        
        if agents_data.empty:
            return self._create_empty_agents_figures()
        
        # 1. Comparaison des agents
        figures['agents_comparison'] = self._create_agents_comparison(agents_data)
        
        # 2. Répartition de la charge de travail
        figures['workload_distribution'] = self._create_workload_distribution(agents_data)
        
        # 3. Analyse de productivité
        figures['productivity_analysis'] = self._create_productivity_analysis(agents_data)
        
        return figures
    
    def _create_agents_comparison(self, df: pd.DataFrame) -> go.Figure:
        """Comparaison des performances des agents"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Volume d\'Appels', 'Performance'],
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        if 'agent' in df:
            agents = df['agent']
            
            # Volume d'appels
            if 'appels_presentes' in df:
                fig.add_trace(
                    go.Bar(x=agents, y=df['appels_presentes'], name='Présentés'),
                    row=1, col=1
                )
            
            if 'appels_traites' in df:
                fig.add_trace(
                    go.Bar(x=agents, y=df['appels_traites'], name='Traités'),
                    row=1, col=1
                )
            
            # Performance (calculée)
            if 'appels_presentes' in df and 'appels_traites' in df:
                performance = (df['appels_traites'] / df['appels_presentes'] * 100).fillna(0)
                fig.add_trace(
                    go.Bar(x=agents, y=performance, name='Taux de Résolution %'),
                    row=1, col=2
                )
        
        fig.update_layout(title="Comparaison des Agents", template=self.template)
        return fig
    
    def _create_workload_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Répartition de la charge de travail"""
        if 'agent' in df and 'appels_presentes' in df:
            fig = px.pie(
                df, 
                values='appels_presentes', 
                names='agent',
                title="Répartition de la Charge de Travail"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
        else:
            fig = go.Figure()
        
        fig.update_layout(template=self.template)
        return fig
    
    def _create_productivity_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Analyse de productivité des agents"""
        fig = go.Figure()
        
        if 'agent' in df and 'appels_traites' in df:
            # Graphique en barres avec gradient
            fig.add_trace(go.Bar(
                x=df['agent'],
                y=df['appels_traites'],
                marker=dict(
                    color=df['appels_traites'],
                    colorscale='Viridis',
                    showscale=True
                ),
                name='Productivité'
            ))
        
        fig.update_layout(
            title="Analyse de Productivité par Agent",
            template=self.template,
            yaxis_title="Nombre d'Appels Traités"
        )
        
        return fig
    
    def _calculate_trends(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calcule les tendances pour les indicateurs"""
        trends = {}
        
        if len(df) < 2:
            return {key: 0 for key in ['volume_trend', 'quality_trend', 'efficiency_trend', 'resources_trend']}
        
        # Tendance volume (appels traités)
        if 'appels_traites' in df:
            first_half = df['appels_traites'][:len(df)//2].mean()
            second_half = df['appels_traites'][len(df)//2:].mean()
            trends['volume_trend'] = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        
        # Tendance qualité (taux de résolution)
        if 'appels_presentes' in df and 'appels_traites' in df:
            taux = df['appels_traites'] / df['appels_presentes'] * 100
            first_half = taux[:len(df)//2].mean()
            second_half = taux[len(df)//2:].mean()
            trends['quality_trend'] = second_half - first_half
        
        # Tendance efficacité (durée - inversée car moins = mieux)
        if 'duree_moyenne_conv' in df:
            first_half = df['duree_moyenne_conv'][:len(df)//2].mean()
            second_half = df['duree_moyenne_conv'][len(df)//2:].mean()
            trends['efficiency_trend'] = -((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        
        # Tendance ressources
        if 'nb_agents_max' in df:
            first_half = df['nb_agents_max'][:len(df)//2].mean()
            second_half = df['nb_agents_max'][len(df)//2:].mean()
            trends['resources_trend'] = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        
        return trends
    
    def _create_empty_figures(self) -> Dict[str, go.Figure]:
        """Crée des figures vides avec messages"""
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            x=0.5, y=0.5,
            text="Aucune donnée disponible",
            showarrow=False,
            font=dict(size=20, color="gray")
        )
        empty_fig.update_layout(template=self.template)
        
        return {
            'volume_calls': empty_fig,
            'temporal_evolution': empty_fig,
            'performance_radar': empty_fig,
            'activity_heatmap': empty_fig,
            'trend_indicators': empty_fig
        }
    
    def _create_empty_agents_figures(self) -> Dict[str, go.Figure]:
        """Crée des figures vides pour les agents"""
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            x=0.5, y=0.5,
            text="Aucune donnée d'agent disponible",
            showarrow=False,
            font=dict(size=20, color="gray")
        )
        empty_fig.update_layout(template=self.template)
        
        return {
            'agents_comparison': empty_fig,
            'workload_distribution': empty_fig,
            'productivity_analysis': empty_fig
        }
    
    def create_executive_summary(self, parsed_data: Dict) -> go.Figure:
        """Crée un résumé exécutif visuel"""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=[
                'Volume Global', 'Taux de Résolution', 'Efficacité Moyenne',
                'Évolution Mensuelle', 'Top Performers', 'Alertes'
            ],
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                [{"type": "scatter"}, {"type": "bar"}, {"type": "table"}]
            ]
        )
        
        # Calcul des KPIs globaux
        monthly_data = parsed_data.get('monthly_data', pd.DataFrame())
        agents_data = parsed_data.get('agents_data', pd.DataFrame())
        
        if not monthly_data.empty:
            total_volume = monthly_data.get('appels_presentes', pd.Series([0])).sum()
            total_traites = monthly_data.get('appels_traites', pd.Series([0])).sum()
            taux_global = (total_traites / total_volume * 100) if total_volume > 0 else 0
            duree_moyenne = monthly_data.get('duree_moyenne_conv', pd.Series([0])).mean()
            
            # Indicateurs KPI
            fig.add_trace(go.Indicator(
                mode="number+gauge",
                value=total_volume,
                title={'text': "Volume Total"},
                gauge={'axis': {'range': [0, total_volume * 1.2]}},
            ), row=1, col=1)
            
            fig.add_trace(go.Indicator(
                mode="number+gauge+delta",
                value=taux_global,
                delta={'reference': 95, 'relative': True},
                title={'text': "Taux Résolution (%)"},
                gauge={'axis': {'range': [80, 100]}},
            ), row=1, col=2)
            
            fig.add_trace(go.Indicator(
                mode="number+gauge",
                value=duree_moyenne,
                title={'text': "Durée Moy. (min)"},
                gauge={'axis': {'range': [0, duree_moyenne * 2]}},
            ), row=1, col=3)
            
            # Évolution mensuelle
            fig.add_trace(go.Scatter(
                x=monthly_data['mois'],
                y=monthly_data.get('appels_traites', []),
                mode='lines+markers',
                name='Évolution',
                line=dict(color=self.color_palette['primary'], width=3)
            ), row=2, col=1)
        
        # Top performers
        if not agents_data.empty and 'agent' in agents_data and 'appels_traites' in agents_data:
            top_agents = agents_data.nlargest(3, 'appels_traites')
            fig.add_trace(go.Bar(
                x=top_agents['agent'],
                y=top_agents['appels_traites'],
                name='Top Performers',
                marker_color=self.color_palette['secondary']
            ), row=2, col=2)
        
        # Table des alertes (simulée)
        alertes = [
            ["Alerte", "Statut"],
            ["Volume Juin", "Pic détecté"],
            ["Agent Performance", "Disparité notée"],
            ["Durée Moyenne", "Dans les normes"]
        ]
        
        fig.add_trace(go.Table(
            header=dict(values=alertes[0], fill_color=self.color_palette['primary']),
            cells=dict(values=list(zip(*alertes[1:])), fill_color='lightgray')
        ), row=2, col=3)
        
        fig.update_layout(
            title="Tableau de Bord Exécutif",
            template=self.template,
            showlegend=False
        )
        
        return fig
    
    def create_comparison_chart(self, data_2024: pd.DataFrame, data_2025: pd.DataFrame) -> go.Figure:
        """Crée un graphique de comparaison année sur année"""
        fig = go.Figure()
        
        if not data_2024.empty and not data_2025.empty:
            months = data_2025.get('mois', [])
            
            fig.add_trace(go.Scatter(
                x=months,
                y=data_2024.get('appels_traites', []),
                mode='lines+markers',
                name='2024',
                line=dict(color=self.color_palette['accent'], width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=months,
                y=data_2025.get('appels_traites', []),
                mode='lines+markers',
                name='2025',
                line=dict(color=self.color_palette['primary'], width=3)
            ))
            
            # Zone de différence
            fig.add_trace(go.Scatter(
                x=months + months[::-1],
                y=list(data_2025.get('appels_traites', [])) + list(data_2024.get('appels_traites', []))[::-1],
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name='Écart'
            ))
        
        fig.update_layout(
            title="Comparaison 2024 vs 2025",
            template=self.template,
            hovermode='x unified'
        )
        
        return fig

# Fonctions utilitaires
def format_duration(minutes: float) -> str:
    """Formate une durée en minutes vers HH:MM"""
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"

def calculate_growth_rate(current: float, previous: float) -> float:
    """Calcule le taux de croissance"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def get_performance_color(value: float, thresholds: Dict[str, float]) -> str:
    """Retourne une couleur basée sur les seuils de performance"""
    if value >= thresholds.get('excellent', 95):
        return '#2ecc71'  # Vert
    elif value >= thresholds.get('good', 85):
        return '#f39c12'  # Orange
    else:
        return '#e74c3c'  # Rouge
