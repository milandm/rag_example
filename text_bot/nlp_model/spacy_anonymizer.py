from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from presidio_anonymizer import DeanonymizeEngine
from presidio_anonymizer.entities import OperatorResult, OperatorConfig
from custom_logger.universal_logger import UniversalLogger
from presidio_analyzer import AnalyzerEngine
from text_bot.nlp_model.spacy_model import get_langugage


WORDS_TO_REMOVE = [
'Qlik',
'Accelerate',
'Lobster',
'ASP',
'Server',
'Equinix',
'Zoho',
'Synerhelp',
'Proxy',
'user']


class SpacyAnonymizer:


    def __init__(self):
        self.analyzer = AnalyzerEngine()

        # Initialize the engine with logger.
        self.anonymize_engine = AnonymizerEngine()

        # Initialize the engine with logger.
        self.deanonymize_engine = DeanonymizeEngine()
        self.logger = UniversalLogger('./log_files/app.log', max_bytes=1048576, backup_count=3)


    def anonymize(self, text):
        self.logger.info("anonymize text "+text)

        language = get_langugage(text)

        # Analyze the text (PII detection)
        analysis_result = self.analyzer.analyze(text=text, entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "COMPANY", "LOCATION", "ADDRESS", "ORG"],
                                           language=language)

        # Anonymize the detected PII entities
        anonymized_result = self.anonymize_engine.anonymize(text=text, analyzer_results=analysis_result)

        self.logger.info("anonymize anonymized_result " + anonymized_result.text)

        # Invoke the anonymize function with the text,
        # analyzer results (potentially coming from presidio-analyzer) and
        # Operators to get the anonymization output:
        result = self.anonymize_engine.anonymize(
            text=text,
            analyzer_results=[
                RecognizerResult(entity_type="PERSON", start=11, end=15, score=0.8),
                RecognizerResult(entity_type="PERSON", start=17, end=27, score=0.8),
            ],
            operators={"PERSON": OperatorConfig("replace", {"new_value": "BIP"})}
        )

        self.logger.info("anonymize result "+result.text)
        return anonymized_result



    def deanonymize(self, text):
        # Invoke the deanonymize function with the text, anonymizer results and
        # Operators to define the deanonymization type.
        result = self.deanonymize_engine.deanonymize(
            text="My name is S184CMt9Drj7QaKQ21JTrpYzghnboTF9pn/neN8JME0=",
            entities=[
                OperatorResult(start=11, end=55, entity_type="PERSON"),
            ],
            operators={"DEFAULT": OperatorConfig("decrypt", {"key": "WmZq4t7w!z%C&F)J"})},
        )

        print("deanonymize result "+result)
        return result





