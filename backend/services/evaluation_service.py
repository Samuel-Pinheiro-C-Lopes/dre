import json
import os
import math
import google.generativeai as genai

class EvaluationService:
    def __init__(self):
        # Initialize Gemini API for embeddings
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)

    @staticmethod
    def cosine_similarity(vec1: list, vec2: list) -> float:
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    def get_embedding(self, text: str) -> list:
        # Use the gemini embedding model
        try:
            result = genai.embed_content(
                model="models/gemini-embedding-2",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding failed: {e}")
            return []

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return EvaluationService.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    @staticmethod
    def levenshtein_similarity(s1: str, s2: str) -> float:
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 100.0
        dist = EvaluationService.levenshtein_distance(s1, s2)
        return ((max_len - dist) / max_len) * 100.0

    def evaluate_and_save(self, extracted_rules: list, correct_rules_path: str, output_path: str):
        # Read correct rules
        if not os.path.exists(correct_rules_path):
            correct_rules = []
        else:
            with open(correct_rules_path, 'r', encoding='utf-8') as f:
                try:
                    correct_rules = json.load(f)
                except json.JSONDecodeError:
                    correct_rules = []

        # 1. Levenshtein Calculation (Baseline)
        def clean_rule(rule):
            return {k: v for k, v in rule.items() if k != "id"}
            
        clean_extracted = [clean_rule(r) for r in extracted_rules]
        clean_correct = [clean_rule(r) for r in correct_rules]

        extracted_str = json.dumps(clean_extracted, sort_keys=True)
        correct_str = json.dumps(clean_correct, sort_keys=True)

        lev_similarity_pct = self.levenshtein_similarity(extracted_str, correct_str)

        # 2. Semantic Similarity Calculation (Recall based on embeddings)
        sem_similarity_pct = 0.0
        match_details = []
        
        if extracted_rules and correct_rules:
            # Generate embeddings for extracted rules
            extracted_embeddings = []
            for er in extracted_rules:
                text = f"{er.get('title', '')}: {er.get('description', '')}"
                embed = self.get_embedding(text)
                if embed:
                    extracted_embeddings.append((er, embed))
                
            total_similarity = 0.0
            
            for cr in correct_rules:
                text = f"{cr.get('title', '')}: {cr.get('description', '')}"
                cr_embed = self.get_embedding(text)
                
                best_match = None
                best_score = 0.0
                
                if cr_embed:
                    for er, er_embed in extracted_embeddings:
                        score = self.cosine_similarity(cr_embed, er_embed)
                        if score > best_score:
                            best_score = score
                            best_match = er
                
                total_similarity += best_score
                match_details.append({
                    "regra_certa_title": cr.get("title", ""),
                    "melhor_match_extraido": best_match.get("title", "") if best_match else None,
                    "score_semantico": round(best_score * 100, 2)
                })
                
            sem_similarity_pct = (total_similarity / len(correct_rules)) * 100.0 if correct_rules else 0.0

        result = {
            "regras_extraidas": extracted_rules,
            "regras_certas": correct_rules,
            "percentual_similaridade_levenshtein": round(lev_similarity_pct, 2),
            "percentual_similaridade_semantica": round(sem_similarity_pct, 2),
            "detalhes_matches_semanticos": match_details
        }

        # Save to output
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
            
        return result
