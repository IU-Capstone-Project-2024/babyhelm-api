import importlib
import pkgutil

routers_list = []

package_name = __name__
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{package_name}.{module_name}")
    if hasattr(module, "router"):
        routers_list.append(module.router)
