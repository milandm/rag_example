from middleware.services.deprecated_search_service import SearchService
from text_bot.nlp_model import OpenaiSdkInterceptor


from text_bot.nlp_model.config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    search_service = SearchService(COLLECTION_NAME, nlp_model)
    print(search_service.search("Cow eats bone"))