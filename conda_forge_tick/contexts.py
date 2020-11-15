import copy
from dataclasses import dataclass
from networkx import DiGraph
import typing
import threading
import github3

from typing import Union

if typing.TYPE_CHECKING:
    from conda_forge_tick.migrators import Migrator
    from conda_forge_tick.migrators_types import AttrsTypedDict


@dataclass
class GithubContext:
    github_username: str
    github_password: str
    circle_build_url: str
    github_token: typing.Optional[str] = ""
    dry_run: bool = True
    _tl: threading.local = threading.local()

    @property
    def gh(self) -> github3.GitHub:
        if getattr(self._tl, "gh", None) is None:
            if self.github_token:
                gh = github3.login(token=self.github_token)
            else:
                gh = github3.login(self.github_username, self.github_password)
            setattr(self._tl, "gh", gh)
        return self._tl.gh

    @property
    def gh_api_requests_left(self) -> Union[int, None]:
        """The remaining API requests left. Returns None if there is an exception"""
        try:
            left = self.gh.rate_limit()["resources"]["core"]["remaining"]
        except Exception:
            left = None

        return left


@dataclass
class MigratorSessionContext(GithubContext):
    """Singleton session context.  There should generally only be one of these"""

    graph: DiGraph = None
    smithy_version: str = ""
    pinning_version: str = ""
    prjson_dir = "pr_json"
    rever_dir: str = "./feedstocks/"
    quiet = True


@dataclass
class MigratorContext:
    """The context for a given migrator.
    This houses the runtime information that a migrator needs
    """

    session: MigratorSessionContext
    migrator: "Migrator"
    _effective_graph: DiGraph = None

    @property
    def github_username(self) -> str:
        return self.session.github_username

    @property
    def effective_graph(self) -> DiGraph:
        # guard this for circular imports
        from conda_forge_tick.migrators import Version

        if self._effective_graph is None:
            gx2 = copy.deepcopy(getattr(self.migrator, "graph", self.session.graph))

            # Prune graph to only things that need builds right now
            for node, node_attrs in self.session.graph.nodes.items():
                with node_attrs["payload"] as attrs:
                    if not isinstance(self.migrator, Version):
                        base_branches = (
                            attrs.get("conda-forge.yml", {})
                            .get("bot", {})
                            .get("abi_migration_branches", [])
                        )
                    else:
                        base_branches = []
                    base_branches = ["master"] + base_branches

                    filters = []
                    try:
                        orig_branch = attrs.get("branch", "master")
                        for base_branch in base_branches:
                            attrs["branch"] = base_branch
                            filters.append(self.migrator.filter(attrs))
                    finally:
                        attrs["branch"] = orig_branch

                if node in gx2 and filters and all(filters):
                    gx2.remove_node(node)
            self._effective_graph = gx2
        return self._effective_graph


@dataclass
class FeedstockContext:
    package_name: str
    feedstock_name: str
    attrs: "AttrsTypedDict"
