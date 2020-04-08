# from x import BP; add to bp list.
from .auth import auth_bp
from .users import users_bp
from .block_files import block_files_bp
from .projects import projects_bp

BLUEPRINTS = [auth_bp, users_bp, projects_bp, block_files_bp]