from flask import Flask
import Config as service_config
from handlers.products import products_blueprint
from handlers.items import items_blueprint
from handlers.meli_auth import meli_auth_blueprint
from handlers.categorys import categories_blueprint
from handlers.custom_queries import custom_queries_blueprint
from handlers.reports import reports_blueprint
from flask_cors import CORS
import databases
import repository


def create_app():
        
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(items_blueprint, url_prefix='/items')
    app.register_blueprint(meli_auth_blueprint, url_prefix='/oauth')
    app.register_blueprint(categories_blueprint, url_prefix='/categories')
    app.register_blueprint(custom_queries_blueprint, url_prefix='/custom-queries')
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
    
    # set products repository
    products_repo = databases.createProductRepository()
    repository.products.setRepository(products_repo)
    
    # set PRs repository
    pr_repo = databases.createPerformanceRecordRepository()
    repository.performance_records.setRepository(pr_repo)
    
    # set IPRs repository
    ipr_repo = databases.createIncompletePerformanceRecordRepository()
    repository.incomplete_performance_records.setRepository(ipr_repo)
    
    # set sellers repository
    sellers_repo = databases.createSellerRepository()
    repository.sellers.setRepository(sellers_repo)
    
    # oauth tokens repository
    oauth_tokens_repo = databases.createMeliOAuthTokenRepository()
    repository.meli_oauth_tokens.setRepository(oauth_tokens_repo)
    
    # custom querys repository
    custom_querys_repo = databases.createCustomQueryRepository()
    repository.custom_querys.setRepository(custom_querys_repo)

    # redis cache
    redis_cache = databases.createRedisCache()
    repository.redis_cache.setCache(redis_cache)

    app.config["JWT_SECRET"] = service_config.JWT_SECRET_KEY
    app.config["SECRET_KEY"] = service_config.FLASK_SECRET_KEY     
    app.config["EXCEL_PATH"] = service_config.EXCEL_PATH   

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=service_config.SERVER_HOST, port=service_config.SERVER_PORT)
    