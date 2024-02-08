from middleware.services.recommendation_service import RecommendationService
from text_bot.nlp_model import OpenaiSdkInterceptor


from text_bot.nlp_model.config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    recommendation_service = RecommendationService(COLLECTION_NAME, nlp_model)
    print(recommendation_service.recommend_history_based())