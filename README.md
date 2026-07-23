# Extrator de Regras (Rule Extractor)

Um sistema completo (Full-Stack) projetado para extrair e estruturar regras, exigências ou diretrizes a partir de documentos jurídicos ou normativos (suporta `.pdf`, `.docx` e `.txt`). A aplicação utiliza a inteligência artificial do **Google Gemini** para leitura e estruturação, apresentando os resultados de forma dinâmica em uma interface moderna feita em React.

## 🚀 Arquitetura

O projeto é dividido em duas partes principais:
1. **Backend (Python / FastAPI)**: Responsável pelo recebimento dos arquivos, extração de texto (via *Chain of Responsibility*), comunicação com a LLM do Gemini e validação de segurança via tokens JWT.
2. **Frontend (React / Vite / Zustand)**: Interface de usuário responsiva e moderna com funcionalidades de Drag-and-Drop, onde o usuário pode subir o documento e visualizar/editar as regras extraídas.

Além disso, o sistema conta com um **Módulo de Avaliação** rigoroso que calcula a Similaridade Semântica (*Cosine Similarity*) e a Distância de Levenshtein entre as regras extraídas pela IA e um gabarito predefinido, garantindo a qualidade da extração.

---

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python 3.14+, FastAPI, Uvicorn, Pydantic, python-jose (JWT), google-generativeai, pdfplumber, python-docx, pytest.
* **Frontend**: Node.js, React 19, TypeScript, Vite, Zustand (Gerenciamento de Estado), Axios, React-Hook-Form, TailwindCSS/Vanilla CSS, Vitest.

---

## ⚙️ Configuração e Instalação

Para rodar a aplicação localmente, certifique-se de ter o Python 3 e o Node.js instalados na sua máquina.

### 1. Configurando o Backend
No diretório raiz do projeto:

```bash
# Entre na pasta do backend
cd backend

# Crie e ative um ambiente virtual (venv)
python3 -m venv venv
source venv/bin/activate  # (No Windows use: venv\Scripts\activate)

# Instale as dependências
pip install -r requirements.txt
```

Crie (ou edite) um arquivo `.env` na raiz do projeto (fora da pasta backend) com as seguintes chaves de segurança:
```env
GOOGLE_API_KEY="sua_chave_do_google_gemini_aqui"
JWT_KEY="chave_criptografica_secreta"
JWT_TOKEN="token_jwt_gerado_com_a_chave"
```

### 2. Configurando o Frontend
No diretório do frontend:

```bash
# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install
```

Crie um arquivo `.env` **dentro da pasta `frontend`** para que o React consiga injetar o token de autorização nas requisições:
```env
VITE_JWT_TOKEN="cole_o_mesmo_token_jwt_gerado_no_backend"
```

---

## ▶️ Executando a Aplicação

A aplicação necessita que tanto o servidor Backend quanto o servidor Frontend estejam rodando simultaneamente.

**Iniciando o Backend (FastAPI):**
Abra um terminal, ative seu ambiente virtual e inicie o servidor na porta 8000.
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```
*O Swagger UI com a documentação da API estará disponível em: http://localhost:8000/docs*

**Iniciando o Frontend (Vite):**
Abra outro terminal e inicie o servidor de desenvolvimento.
```bash
cd frontend
npm run dev
```
*A interface web estará disponível em: http://localhost:5173*

---

## 🧪 Testes Automatizados e Avaliação (Evaluation)

O projeto conta com uma suíte de testes robusta que não apenas verifica se os endpoints estão funcionando, mas também avalia a qualidade da IA ao ler um documento e extrair as regras (usando um gabarito presente em `backend/resources/rules.json`).

Para rodar a avaliação de Similaridade Semântica e Levenshtein:
```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest backend/test_api.py -v -s
```
Os resultados da avaliação (Score de similaridade e detalhes dos matches) serão salvos automaticamente em `backend/output/results.json`.
Para rodar os testes da interface:
```bash
cd frontend
npm run test
```
