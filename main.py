"""
Application FastAPI suivant le pattern MVC
Point d'entrée principal de l'application
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from config.app_config import app_config
from controllers.main_controller import MainController
from controllers.auth_controller import AuthController
from controllers.produit_controller import ProduitController


def create_app() -> FastAPI:
    """
    Fonction factory pour créer et configurer l'application FastAPI
    
    Returns:
        Instance configurée de FastAPI
    """
    # Création de l'application FastAPI
    app = FastAPI(
        title="Application de connexion MVC",
        description="Application démonstrant le pattern MVC avec FastAPI",
        version="1.0.0"
    )
    
    # Configuration du middleware de session
    app.add_middleware(
        SessionMiddleware, 
        secret_key=app_config.SECRET_KEY
    )
    
    # Configuration des fichiers statiques
    app.mount(
        app_config.STATIC_URL, 
        StaticFiles(directory=app_config.STATIC_DIR), 
        name="static"
    )
    
    # Configuration des templates
    templates = Jinja2Templates(directory=app_config.TEMPLATES_DIR)
    
    # Initialisation des contrôleurs
    main_controller = MainController(templates)
    auth_controller = AuthController(templates)
    produit_controller = ProduitController(templates)
    
    # Enregistrement des routes
    register_routes(app, main_controller, auth_controller, produit_controller)
    
    return app


def register_routes(app: FastAPI, main_controller: MainController, auth_controller: AuthController, produit_controller: ProduitController):
    """
    Enregistre toutes les routes de l'application
    
    Args:
        app: Instance FastAPI
        main_controller: Contrôleur principal
        auth_controller: Contrôleur d'authentification
    """
    # Routes principales
    app.add_api_route(
        "/", 
        main_controller.home, 
        methods=["GET"], 
        response_class=HTMLResponse,
        name="home"
    )
    
    # Routes d'authentification
    app.add_api_route(
        "/login", 
        auth_controller.login_form, 
        methods=["GET"], 
        response_class=HTMLResponse,
        name="login_form"
    )
    
    app.add_api_route(
        "/login", 
        auth_controller.login, 
        methods=["POST"],
        name="login_post"
    )
    
    app.add_api_route(
        "/logout", 
        auth_controller.logout, 
        methods=["GET"],
        name="logout"
    )
    
    app.add_api_route(
        "/register", 
        auth_controller.register_form, 
        methods=["GET"], 
        response_class=HTMLResponse,
        name="register_form"
    )
    
    app.add_api_route(
        "/register", 
        auth_controller.register, 
        methods=["POST"],
        name="register_post"
    )
    
    app.add_api_route(
        "/produits",
        produit_controller.list_produits,
        methods=["GET"],
        response_class=HTMLResponse,
        name="list_produits"
    )
    
    app.add_api_route(
        "/produits/add",
        produit_controller.add_produit_form,
        methods=["GET"],
        response_class=HTMLResponse,
        name="add_produit_form"
    )
    
    app.add_api_route(
        "/produits/add",
        produit_controller.add_produit,
        methods=["POST"],
        name="add_produit_post"
    )
    
    app.add_api_route(
        "/produits/{id}/delete",
        produit_controller.delete_produit,
        methods=["GET", "POST"],
        name="delete_produit"
    )
    
    app.add_api_route(
        "/produits/{id}",
        produit_controller.view_produit,
        methods=["GET"],
        response_class=HTMLResponse,
        name="view_produit"
    )
    
    app.add_api_route(
        "/produits/{id}/edit",
        produit_controller.edit_produit_form,
        methods=["GET"],
        response_class=HTMLResponse,
        name="edit_produit_form"
    )
    
    app.add_api_route(
        "/produits/{id}/edit",
        produit_controller.edit_produit,
        methods=["POST"],
        name="edit_produit_post"
    )


# Création de l'instance de l'application
app = create_app()


# Point d'entrée pour le développement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )

# cmd : uvicorn main:app --reload