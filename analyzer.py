from typing import Dict, List, Tuple
import numpy as np
from collections import Counter
import re
from unicodedata import normalize
from database import sample_texts

class SpellingPatternAnalyzer:
    def __init__(self):
        # Patrones comunes de errores ortográficos en español
        self.common_patterns = {
            'b_v': [
                (r'\bb(\w*)', r'v\1'),  # biene -> viene
                (r'\bv(\w*)', r'b\1'),  # vien -> bien
            ],
            'h_silent': [
                (r'\bh(\w+)', r'\1'),    # haber -> aber
                (r'\b([aeiou]\w+)', r'h\1'),  # asta -> hasta
            ],
            'll_y': [
                (r'll', 'y'),  # llegar -> yegar
                (r'y', 'll'),  # yave -> llave
            ],
            's_c_z': [
                (r'c([ei])', r's\1'),  # cecina -> sesina
                (r'z([aou])', r's\1'),  # zapato -> sapato
                (r's([ei])', r'c\1'),  # sena -> cena
            ],
            'g_j': [
                (r'g([ei])', r'j\1'),  # gente -> jente
                (r'j([ei])', r'g\1'),  # jeneral -> general
            ],
            'tildes': [
                ('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
                ('a', 'á'), ('e', 'é'), ('i', 'í'), ('o', 'ó'), ('u', 'ú'),
            ],
            'puntuacion': [
                (r'¿', ''), (r'¡', ''),  # Omisión de signos de apertura
                (r',', ''), (r';', ''),  # Omisión de puntuación
            ]
        }

    def find_spelling_patterns(self, text: str) -> Dict[str, List[Tuple[str, str]]]:
        """
        Analiza el texto en busca de patrones de errores ortográficos.

        Args:
            text (str): Texto a analizar

        Returns:
            Dict[str, List[Tuple[str, str]]]: Diccionario con categorías de errores y sus instancias
        """
        patterns_found = {category: [] for category in self.common_patterns.keys()}
        words = text.lower().split()

        for word in words:
            norm_word = normalize('NFKD', word).encode('ASCII', 'ignore').decode('ASCII')

            for category, patterns in self.common_patterns.items():
                for pattern, replacement in patterns:
                    if re.search(pattern, word):
                        potential_error = re.sub(pattern, replacement, word)
                        if potential_error != word:
                            patterns_found[category].append((word, potential_error))

        return patterns_found

class TextStyleAnalyzer:
    def __init__(self):
        self.spanish_stopwords = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o',
            'pero', 'porque', 'que', 'de', 'a', 'en', 'con', 'por', 'para', 'del',
            'al', 'lo', 'le', 'se', 'su', 'sus', 'mi', 'mis', 'tu', 'tus'
        }
        self.spelling_analyzer = SpellingPatternAnalyzer()

    def analyze_text(self, text: str) -> Dict:
        """
        Realiza un análisis completo de un texto.

        Args:
            text (str): Texto a analizar

        Returns:
            Dict: Resultados del análisis
        """
        # Análisis básico
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])

        # Análisis de errores ortográficos
        spelling_patterns = self.spelling_analyzer.find_spelling_patterns(text)

        # Estadísticas de texto
        stats = {
            **self.get_sentence_length_stats(text),
            **self.get_word_frequency_stats(text)
        }

        return {
            'basic_stats': {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'avg_words_per_sentence': word_count / sentence_count if sentence_count > 0 else 0
            },
            'spelling_patterns': spelling_patterns,
            'text_stats': stats
        }

    def analyze_against_database(self, input_text: str, min_similarity: float = 70.0) -> List[Dict]:
        """
        Compara un texto de entrada contra la base de datos de textos conocidos.

        Args:
            input_text (str): Texto a comparar
            min_similarity (float): Umbral mínimo de similitud (0-100)

        Returns:
            List[Dict]: Lista de coincidencias que superan el umbral
        """
        matches = []

        for sample in sample_texts:
            similarity_score, detailed_scores = self.calculate_similarity_score(
                input_text, sample['texto']
            )

            if similarity_score * 100 >= min_similarity:
                matches.append({
                    'id': sample['id'],
                    'autor': sample['autor'],
                    'similitud': similarity_score * 100,
                    'detalles': detailed_scores
                })

        # Ordenar por similitud descendente
        matches.sort(key=lambda x: x['similitud'], reverse=True)
        return matches

    def preprocess_text(self, text: str) -> str:
        """Preprocesa el texto para análisis."""
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s\.]', '', text)
        return text

    def get_sentence_length_stats(self, text: str) -> Dict[str, float]:
        """Calcula estadísticas sobre la longitud de las oraciones."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        lengths = [len(s.split()) for s in sentences]

        return {
            'avg_sentence_length': np.mean(lengths) if lengths else 0,
            'std_sentence_length': np.std(lengths) if lengths else 0,
            'max_sentence_length': max(lengths) if lengths else 0,
            'min_sentence_length': min(lengths) if lengths else 0
        }

    def get_word_frequency_stats(self, text: str) -> Dict[str, float]:
        """Calcula estadísticas sobre frecuencia de palabras."""
        words = [w for w in text.split() if w not in self.spanish_stopwords]
        freq = Counter(words)

        return {
            'unique_words_ratio': len(set(words)) / len(words) if words else 0,
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'common_words': set(dict(freq.most_common(10)).keys())
        }

    def calculate_similarity_score(self, text1: str, text2: str) -> Tuple[float, Dict]:
        """
        Calcula la similitud entre dos textos.

        Args:
            text1 (str): Primer texto
            text2 (str): Segundo texto

        Returns:
            Tuple[float, Dict]: Score de similitud (0-1) y detalles del cálculo
        """
        # Análisis de errores ortográficos
        spelling_patterns1 = self.spelling_analyzer.find_spelling_patterns(text1)
        spelling_patterns2 = self.spelling_analyzer.find_spelling_patterns(text2)
        spelling_sim = self._compare_spelling_patterns(spelling_patterns1, spelling_patterns2)

        # Preprocesar textos
        proc_text1 = self.preprocess_text(text1)
        proc_text2 = self.preprocess_text(text2)

        # Obtener estadísticas
        stats1 = {**self.get_sentence_length_stats(proc_text1),
                 **self.get_word_frequency_stats(proc_text1)}
        stats2 = {**self.get_sentence_length_stats(proc_text2),
                 **self.get_word_frequency_stats(proc_text2)}

        # Calcular similitudes individuales
        sentence_length_sim = self._safe_similarity(
            stats1['avg_sentence_length'],
            stats2['avg_sentence_length']
        )
        word_length_sim = self._safe_similarity(
            stats1['avg_word_length'],
            stats2['avg_word_length']
        )
        unique_words_sim = self._safe_similarity(
            stats1['unique_words_ratio'],
            stats2['unique_words_ratio']
        )
        common_words_sim = len(
            stats1['common_words'].intersection(stats2['common_words'])
        ) / 10

        # Pesos para cada métrica
        weights = {
            'sentence_length': 0.2,
            'word_length': 0.15,
            'unique_words': 0.2,
            'common_words': 0.15,
            'spelling_patterns': 0.3
        }

        # Calcular score final
        final_score = (
            weights['sentence_length'] * sentence_length_sim +
            weights['word_length'] * word_length_sim +
            weights['unique_words'] * unique_words_sim +
            weights['common_words'] * common_words_sim +
            weights['spelling_patterns'] * spelling_sim
        )

        detailed_scores = {
            'sentence_length_similarity': sentence_length_sim,
            'word_length_similarity': word_length_sim,
            'unique_words_similarity': unique_words_sim,
            'common_words_similarity': common_words_sim,
            'spelling_patterns_similarity': spelling_sim,
            'raw_patterns': {
                'text1': spelling_patterns1,
                'text2': spelling_patterns2
            }
        }

        return final_score, detailed_scores

    def _compare_spelling_patterns(self, patterns1: Dict, patterns2: Dict) -> float:
        """Compara patrones de errores ortográficos entre dos textos."""
        similarity_scores = []

        for category in patterns1.keys():
            # Calcular similitud basada en la presencia de tipos similares de errores
            has_pattern1 = bool(patterns1[category])
            has_pattern2 = bool(patterns2[category])

            if has_pattern1 and has_pattern2:
                similarity_scores.append(1.0)
            elif not has_pattern1 and not has_pattern2:
                similarity_scores.append(1.0)
            else:
                similarity_scores.append(0.0)

        return np.mean(similarity_scores) if similarity_scores else 0.0

    def _safe_similarity(self, val1: float, val2: float) -> float:
        """Calcula similitud entre dos valores de manera segura."""
        if val1 == val2:
            return 1.0
        if val1 == 0 and val2 == 0:
            return 1.0
        if val1 == 0 or val2 == 0:
            return 0.0
        return 1 - abs(val1 - val2) / max(val1, val2)

def format_analysis_results(results: List[Dict]) -> str:
    """
    Formatea los resultados del análisis para presentación.

    Args:
        results (List[Dict]): Lista de resultados de análisis

    Returns:
        str: Resultados formateados para mostrar
    """
    if not results:
        return "No se encontraron coincidencias significativas."

    output = []
    for match in results:
        output.append(f"\nCoincidencia con Autor: {match['autor']}")
        output.append(f"Porcentaje de similitud: {match['similitud']:.2f}%")
        output.append("\nDetalles de la similitud:")
        for key, value in match['detalles'].items():
            if key != 'raw_patterns':
                output.append(f"- {key}: {value:.2f}")

        output.append("\nPatrones de errores ortográficos encontrados:")
        for category, errors in match['detalles']['raw_patterns']['text1'].items():
            if errors:
                output.append(f"\n{category}:")
                for original, correction in errors[:5]:  # Mostrar solo los primeros 5 ejemplos
                    output.append(f"  {original} -> {correction}")

    return "\n".join(output)