#!/usr/bin/env python3
"""Github API client for fetching organization information."""
from typing import Dict, List, Optional
from utils import get_json


class GithubOrgClient:
    """A client for accessing GitHub organization information.

    This client provides methods to retrieve information about a GitHub
    organization, including public repositories and license information.
    """

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize the GithubOrgClient with an organization name.

        Args:
            org_name: The name of the GitHub organization.
        """
        self._org_name = org_name
        self._org: Optional[Dict] = None

    @property
    def org(self) -> Dict:
        """Get the organization information from GitHub API.

        Returns:
            A dictionary containing the organization information.
        """
        if self._org is None:
            self._org = get_json(self.ORG_URL.format(self._org_name))
        return self._org

    @property
    def _public_repos_url(self) -> str:
        """Get the URL for public repositories of the organization.

        Returns:
            The URL string for public repositories.
        """
        return self.org["repos_url"]

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Get the list of public repository names for the organization.

        Args:
            license: Optional license key to filter repositories.

        Returns:
            A list of repository names matching the criteria.
        """
        repos_json = get_json(self._public_repos_url)
        repos = [repo["name"] for repo in repos_json]

        if license is not None:
            repos = [
                repo["name"]
                for repo in repos_json
                if self.has_license(repo, license)
            ]

        return repos

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if a repository has a specific license.

        Args:
            repo: A dictionary containing repository information.
            license_key: The license key to check for.

        Returns:
            True if the repository has the specified license, False otherwise.
        """
        if "license" not in repo:
            return False
        return repo.get("license", {}).get("key") == license_key

