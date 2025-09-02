import PyPDF2
import re
import pandas as pd
import pdfplumber
from typing import Dict, List, Tuple, Optional
import numpy as np
from datetime import datetime

class TelephoneReportParser:
    """Parser spécialisé pour les rapports de téléphonie"""
    
    def __init__(self):
        self.months_fr = {
            'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4,
            'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8,
            'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
        }
    
    def parse_pdf(self, pdf_file) -> Dict:
        """Parse le PDF et extrait toutes les données structurées"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text_content = self._extract_all_text(pdf)
                tables_data = self._extract_tables(pdf)
                
                # Extraction des différents types de données
                monthly_data = self._extract_monthly_data(text_content, tables_data)
                agents_data = self._extract_agents_data(text_content, tables_data)
                kpi_data = self._extract_kpi_data(text_content)
                resolution_data = self._extract_resolution_data(text_content, tables_data)
                tickets_data = self._extract_tickets_data(tables_data)
                
                return {
                    'monthly_data': monthly_data,
                    'agents_data': agents_data,
                    'kpi_data': kpi_data,
                    'resolution_data': resolution_data,
                    'tickets_data': tickets_data,
                    'parsing_success': True
                }
        except Exception as e:
            print(f"Erreur lors du parsing: {e}")
            return {'parsing_success': False, 'error': str(e)}
    
    def _extract_all_text(self, pdf) -> str:
        """Extrait tout le texte du PDF"""
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""
        return full_text
    
    def _extract_tables(self, pdf) -> List[List[List]]:
        """Extrait toutes les tables du PDF"""
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                all_tables.extend(tables)
        return all_tables
    
    def _extract_monthly_data(self, text: str, tables: List) -> pd.DataFrame:
        """Extrait les données mensuelles d'activité"""
        monthly_data = []
        
        # Pattern pour capturer les données mensuelles
        patterns = {
            'appels_traites': r'Appels Traités vs Présentés.*?(\d+).*?(\d+)',
            'duree_conversation': r'Durée Moyenne de Conversation.*?(\d+):(\d+):(\d+)',
            'nb_agents': r'Nombre d\'Agents Max.*?(\d+)'
        }
        
        # Recherche des sections mensuelles
        month_sections = re.findall(r'(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s+2025\s+Agents(.*?)(?=(?:Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s+2025\s+Agents|Cloture|$)', 
                                   text, re.DOTALL)
        
        for month_name, section_text in month_sections:
            month_data = {'mois': month_name}
            
            # Extraction des appels traités vs présentés
            appels_match = re.search(r'(\d+).*?(\d+)', section_text)
            if appels_match:
                month_data['appels_traites'] = int(appels_match.group(1))
                month_data['appels_presentes'] = int(appels_match.group(2))
            
            # Extraction durée conversation
            duree_match = re.search(r'(\d+):(\d+):(\d+)', section_text)
            if duree_match:
                minutes = int(duree_match.group(2))
                seconds = int(duree_match.group(3))
                month_data['duree_moyenne_conv'] = round(minutes + seconds/60, 2)
            
            # Extraction nombre d'agents
            agents_match = re.search(r'Nombre d\'Agents Max.*?(\d+)', section_text)
            if agents_match:
                month_data['nb_agents_max'] = int(agents_match.group(1))
            
            if len(month_data) > 1:  # Si on a trouvé des données
                monthly_data.append(month_data)
        
        return pd.DataFrame(monthly_data) if monthly_data else pd.DataFrame()
    
    def _extract_agents_data(self, text: str, tables: List) -> pd.DataFrame:
        """Extrait les données individuelles des agents"""
        agents_data = []
        
        # Recherche des tableaux détaillés d'agents
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            # Vérification si c'est un tableau d'agents
            header = table[0] if table[0] else []
            if any('Agent' in str(cell) for cell in header if cell):
                agents_data = self._parse_agents_table(table)
                break
        
        # Si pas de tableau trouvé, extraction via regex
        if not agents_data:
            agents_data = self._extract_agents_from_text(text)
        
        return pd.DataFrame(agents_data) if agents_data else pd.DataFrame()
    
    def _parse_agents_table(self, table: List[List]) -> List[Dict]:
        """Parse un tableau d'agents structuré"""
        agents = []
        headers = [cell.strip() if cell else '' for cell in table[0]]
        
        for row in table[1:]:
            if not row or not any(row):
                continue
                
            agent_data = {}
            for i, cell in enumerate(row):
                if i < len(headers) and headers[i] and cell:
                    agent_data[headers[i]] = cell.strip()
            
            if agent_data:
                agents.append(agent_data)
        
        return agents
    
    def _extract_agents_from_text(self, text: str) -> List[Dict]:
        """Extraction des agents depuis le texte brut"""
        agents = []
        
        # Patterns pour les noms d'agents connus
        agent_patterns = [
            'FABIENNE COCQUART',
            'PHILIPPE KUBLER', 
            'Sebastien SIE',
            'Franck PAIRA'
        ]
        
        for agent_name in agent_patterns:
            # Recherche des données de cet agent
            agent_section = re.search(f'{agent_name}.*?(?={"|".join(agent_patterns)}|$)', text, re.DOTALL | re.IGNORECASE)
            if agent_section:
                agent_text = agent_section.group(0)
                
                agent_data = {'agent': agent_name}
                
                # Extraction des métriques
                numbers = re.findall(r'\b(\d+)\b', agent_text)
                if len(numbers) >= 2:
                    agent_data['appels_presentes'] = int(numbers[0]) if numbers else 0
                    agent_data['appels_traites'] = int(numbers[1]) if len(numbers) > 1 else 0
                
                agents.append(agent_data)
        
        return agents
    
    def _extract_kpi_data(self, text: str) -> Dict:
        """Extrait les KPI globaux"""
        kpi = {}
        
        # Extraction du taux de résolution global
        resolution_match = re.search(r'(\d+,?\d*)%', text)
        if resolution_match:
            kpi['taux_resolution_global'] = float(resolution_match.group(1).replace(',', '.'))
        
        # Moyennes mensuelles
        moyennes_section = re.search(r'Moyennes Mensuelles.*?(\d+,\d+).*?(\d+,\d+)', text)
        if moyennes_section:
            kpi['moyenne_appels_recus'] = float(moyennes_section.group(1).replace(',', '.'))
            kpi['moyenne_appels_resolus'] = float(moyennes_section.group(2).replace(',', '.'))
        
        return kpi
    
    def _extract_resolution_data(self, text: str, tables: List) -> pd.DataFrame:
        """Extrait les données de résolution des appels"""
        resolution_data = []
        
        # Recherche du tableau de résolution
        for table in tables:
            if not table:
                continue
                
            # Vérification si c'est le tableau de résolution
            if any('résolus par N1' in str(cell) for row in table for cell in row if cell):
                for i, row in enumerate(table[1:], 1):  # Skip header
                    if row and len(row) >= 4:
                        try:
                            resolution_data.append({
                                'mois': i,
                                'n2': int(row[1]) if row[1] and str(row[1]).isdigit() else 0,
                                'appels': int(row[2]) if row[2] and str(row[2]).isdigit() else 0,
                                'resolus_n1': int(row[3]) if row[3] and str(row[3]).isdigit() else 0,
                                'pourcentage': float(row[4].replace('%', '').replace(',', '.')) if row[4] else 0
                            })
                        except (ValueError, IndexError):
                            continue
                break
        
        return pd.DataFrame(resolution_data) if resolution_data else pd.DataFrame()
    
    def _extract_tickets_data(self, tables: List) -> pd.DataFrame:
        """Extrait les données des tickets N2"""
        tickets_data = []
        
        for table in tables:
            if not table:
                continue
                
            # Vérification si c'est le tableau des tickets
            if any('Tickets' in str(cell) and 'N2' in str(cell) for row in table for cell in row if cell):
                # Parse le tableau des tickets
                for row in table[1:]:  # Skip header
                    if row and len(row) >= 8:
                        try:
                            day_data = {
                                'jour': int(row[0]) if row[0] and str(row[0]).isdigit() else 0
                            }
                            
                            # Ajouter les données mensuelles
                            for month_idx in range(1, min(9, len(row))):
                                if row[month_idx] and str(row[month_idx]).isdigit():
                                    day_data[f'mois_{month_idx}'] = int(row[month_idx])
                            
                            if day_data['jour'] > 0:
                                tickets_data.append(day_data)
                        except (ValueError, IndexError):
                            continue
                break
        
        return pd.DataFrame(tickets_data) if tickets_data else pd.DataFrame()
    
    def get_summary_statistics(self, parsed_data: Dict) -> Dict:
        """Calcule des statistiques de résumé"""
        stats = {}
        
        if 'monthly_data' in parsed_data and not parsed_data['monthly_data'].empty:
            monthly_df = parsed_data['monthly_data']
            
            stats['total_appels_presentes'] = monthly_df['appels_presentes'].sum() if 'appels_presentes' in monthly_df else 0
            stats['total_appels_traites'] = monthly_df['appels_traites'].sum() if 'appels_traites' in monthly_df else 0
            stats['duree_moyenne_globale'] = monthly_df['duree_moyenne_conv'].mean() if 'duree_moyenne_conv' in monthly_df else 0
            stats['taux_resolution_calcule'] = (stats['total_appels_traites'] / stats['total_appels_presentes'] * 100) if stats['total_appels_presentes'] > 0 else 0
        
        if 'agents_data' in parsed_data and not parsed_data['agents_data'].empty:
            agents_df = parsed_data['agents_data']
            stats['nombre_agents_actifs'] = len(agents_df)
            
            if 'appels_presentes' in agents_df:
                stats['agent_le_plus_actif'] = agents_df.loc[agents_df['appels_presentes'].idxmax(), 'agent'] if not agents_df.empty else 'N/A'
        
        return stats

def test_parser():
    """Fonction de test du parser"""
    parser = TelephoneReportParser()
    
    # Test avec données simulées
    sample_text = """
    Janvier 2025 Agents
    Appels Traités vs Présentés
    570 ▼ 594
    Durée Moyenne de Conversation
    00:05:51
    Nombre d'Agents Max
    3
    """
    
    # Simulation d'extraction
    result = parser._extract_monthly_data(sample_text, [])
    print("Test du parser:")
    print(result)

if __name__ == "__main__":
    test_parser()
