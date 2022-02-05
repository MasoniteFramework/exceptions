import pkg_resources
import requests

from .Block import Block


def get_latest_version(name):
    r = requests.get(f"https://pypi.org/pypi/{name}/json")
    if r.status_code == 200:
        version = r.json()["info"]["version"]
        return version
    return None


class PackagesUpdates(Block):
    id = "packages_updates"
    name = "Packages to update"
    icon = "ArrowCircleUpIcon"
    component = "PackagesUpdatesBlock"

    def build(self):
        installed_packages = {
            package.key: package.version for package in pkg_resources.working_set
        }
        packages_to_check = self.handler.options.get("blocks.packages_updates.list", [])
        packages = {}
        if packages_to_check:
            #     with open(".pyexceptions.packages", "r+") as f:
            #         data = f.read()
            #         if data:
            #             versions = loads(data)
            #         else:
            #             versions = {}
            for package_name in packages_to_check:
                # latest_version = versions.get(package.project_name)
                # if not latest_version:
                current_version = installed_packages.get(package_name)
                latest_version = get_latest_version(package_name)
                if current_version != latest_version:
                    packages.update(
                        {
                            package_name: {
                                "current": installed_packages.get(package_name),
                                "latest": latest_version,
                            }
                        }
                    )
        #         json.dump(versions, f)

        return packages

    def has_content(self):
        return len(self.data.keys()) > 0
