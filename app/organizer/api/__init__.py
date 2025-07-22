from flask import Blueprint

from .auth import BP as auth_bp
from .meals import BP as meals_bp
from .products import BP as products_bp
from .trips import BP as trips_bp
from .reports import BP as reports_bp
from .users import BP as users_bp
from .maintenance import BP as maintenance_bp

BP = Blueprint("api", __name__, url_prefix="/api")

BP.register_blueprint(auth_bp)
BP.register_blueprint(trips_bp)
BP.register_blueprint(meals_bp)
BP.register_blueprint(products_bp)
BP.register_blueprint(reports_bp)
BP.register_blueprint(users_bp)
BP.register_blueprint(maintenance_bp)
