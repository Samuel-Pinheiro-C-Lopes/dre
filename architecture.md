## PAGES
- **Rule extractor:** it must receive a document as an input before generating filled rules input fields and an option to add new rules manually, besides removing and editing the already created rules.

## LAYERS

### BACKEND
- **LLM engine:** will be an interface for the LLM. This interface will be implemented for each LLM specific configurations and properties. Start with a Gemini implementation. Uses a LLMEngine interface.
- **Document Engine:** since it will be needed to read the content of different document extensions, use the Chain of Responsability pattern through a DocumentEngine interface in which each implementation will be responsible for each extensions. Implement already one for pdf, other for .docx and one for .txt.
- **service:** There are going to be three services: 
    **LLMService:** deals with LLM calls to extract rules from a document using the specific prompt received from the caller and using the LLM injected;
    **DocumentService:** deals with the text extraction from the document, receiving the file and returning the resulting text; and
    **ExtractionService:** orquestrator that uses the LLMService alongside with the DocumentService, parametrizing them and calling their methods to return the extracted rules. It must load the prompt used from a .txt file - and use the documentservice to obtain the content - from a /resources/prompt.txt path. Once obtained the prompt from the file, it must hold both the content and the last edited date of the file as state to avoid fetching it again without need.
- **controller:** RuleExtractorController will be the single controller that will expose a post method to receive a document and return a list of rules within a RulesResponse.
- **configuration:** the configuration layer / module is responsible for the code artifacts assigning the Documentation Swagger API for easy testing and the authentication / authorization that will only allow post requests through the RuleExtractorController's post method - and only method. 

### FRONTEND
- **pages:** pages layer that will cotnain only the rule extractor page, being that the home page as well.
- **services:** api service will be the manager of requests while the state service will hold the data received by the api service and, afterwards, shall make it available for the rule extractor page. The state will be the single source of truth.